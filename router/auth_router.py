import base64
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Form, Request, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
import jwt
from pydantic import BaseModel
from passlib.context import CryptContext

from core.config import settings
from core.security import limiter

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

api_auth = APIRouter(tags=["Authenticate"])

users_db = {
    "admin": {
        "id": 99,
        "username": "admin",
        "hashed_password": pwd_context.hash("admin123"),
        "role": "admin",
        "mfa_secret": "123456",
        "scopes": "events:read events:write events:sync-inventory"
    },
    "alice": {
        "id": 1,
        "username": "alice",
        "hashed_password": pwd_context.hash("senha123"),
        "role": "organizador",
        "mfa_secret": None,
        "scopes": "events:read events:write"
    },
    "bob": {
        "id": 2,
        "username": "bob",
        "hashed_password": pwd_context.hash("senha123"),
        "role": "participante",
        "mfa_secret": None,
        "scopes": "events:read"
    }
}

m2m_clients_db = {
    "partner_client_id": {
        "client_secret": "partner_secret_123",
        "scopes": "events:read events:sync-inventory"
    }
}

class User(BaseModel):
    id: int
    username: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def decode_jwt(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_token_claims(security_scopes: SecurityScopes, token_payload: dict = Depends(decode_jwt)):
    token_scopes = token_payload.get("scope", "").split()
    for required_scope in security_scopes.scopes:
        if required_scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Escopo insuficiente. Requer: {required_scope}"
            )

    if token_payload.get("grant_type") == "client_credentials":
        return token_payload

    user_role = token_payload.get("role")
    if user_role not in ["organizador", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Perfil de usuário sem permissão."
        )

    return token_payload

@api_auth.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    mfa_code: Optional[str] = Form(None)
):
    if form_data.grant_type == "client_credentials" or form_data.client_id:
        client_id = form_data.client_id or form_data.username
        client_secret = form_data.client_secret or form_data.password
        
        client = m2m_clients_db.get(client_id)
        if not client or client["client_secret"] != client_secret:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais M2M inválidas.",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        access_token = create_access_token(
            data={"sub": client_id, "grant_type": "client_credentials", "scope": client["scopes"]}
        )
        return {"access_token": access_token, "token_type": "bearer"}

    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    mfa_enviado = mfa_code or form_data.client_secret
    if not mfa_enviado:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Basic "):
            try:
                encoded = auth_header.split(" ")[1]
                decoded = base64.b64decode(encoded).decode("utf-8")
                if ":" in decoded:
                    mfa_enviado = decoded.split(":", 1)[1]
            except Exception:
                pass

    mfa_validado = mfa_enviado.strip() if mfa_enviado and str(mfa_enviado).strip() else None

    if user.get("role") == "admin":
        if not mfa_validado or mfa_validado != user.get("mfa_secret"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Código MFA obrigatório e/ou inválido para contas de administrador.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    access_token = create_access_token(
        data={
            "sub": user["username"],
            "user_id": user["id"],
            "role": user["role"],
            "scope": user["scopes"],
            "grant_type": "password"
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}

@api_auth.post("/events/sync", dependencies=[Security(verify_token_claims, scopes=["events:sync-inventory"])])
async def sync_partner_inventory():
    return {"status": "Sincronização realizada com sucesso"}

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_jwt(token)
    username: str = payload.get("sub")
    user_id: int = payload.get("user_id")
    role: str = payload.get("role")
    
    if username is None or user_id is None or role is None:
        raise credentials_exception
        
    return User(id=user_id, username=username, role=role)

def check_ownership(resource_owner_id: int, current_user: User):
    if current_user.role == "admin":
        return True
    if current_user.id != resource_owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Você não possui permissão para este recurso."
        )
    return True