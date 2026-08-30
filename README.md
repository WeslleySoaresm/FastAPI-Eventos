

## 🖥️ Interface de Usuário (UI)

Além dos endpoints RESTful, a aplicação conta com uma interface Web acessível via navegador:

* **`/event/ui`**: Painel principal para listagem de todos os eventos cadastrados.
* **`/event/ui/new`**: Formulário interativo estilizado com **Tailwind CSS** para cadastro de novos eventos sem necessidade de depender do Swagger.
* **`/event/ui/audit`**: Relatório de Auditoria de Segurança focado nos pilares CIA (Confidencialidade, Integridade e Disponibilidade).

```

---


# 📅 FastAPI Eventos API (`FastAPI-Eventos`)

**Disciplina:** Arquitetura e Segurança de APIs REST com FastAPI — TP1  
**Repositório:** `FastAPI-Eventos`

API RESTful e aplicação web desenvolvida em **FastAPI** e **Pydantic** para gerenciamento de eventos. O projeto contempla operações completas de CRUD, validação de dados em tempo de execução, controle de exposição de dados sensíveis, interface web interativa renderizada com **Jinja2** e **Tailwind CSS**, além de arquitetura de segurança alinhada aos frameworks **OWASP**, **NIST SSDF** e **MITRE ATT&CK**.

---

## 🛠️ Arquitetura e Módulos do Projeto

| Arquivo / Diretório | Camada | Responsabilidade Principal |
| :--- | :--- | :--- |
| `main.py` | **Aplicação** | Ponto de entrada (`entrypoint`). Instancia o `FastAPI()`, inclui as rotas registradas no `APIRouter` e define endpoints globais como o status do serviço (`GET /`). |
| `data/db.py` | **Persistência** | Responsável pelo armazenamento e gerenciamento do estado dos dados. Mantém as coleções em memória (listas Python) e abstrai a manipulação de leitura e escrita da camada de roteamento. |
| `models/events.py` | **Domínio / Validação** | Define os esquemas de dados utilizando **Pydantic (`BaseModel`)**. Garante a tipagem estrita dos campos do evento, define valores padrão e aplica o `response_model` para controle de segurança. |
| `models/users.py` | **Domínio / Validação** | Define esquemas Pydantic voltados aos usuários e organizadores do sistema. |
| `router/events.py` | **Controlador (API & UI)** | Contém as definições das rotas HTTP RESTful (`GET`, `POST`, `PUT`, `DELETE`) e rotas HTML (`/event/ui`, `/event/ui/new`, `/event/ui/audit`). Trata `Form(...)`, exibe `HTTPException` e gerencia redirecionamentos (`RedirectResponse`). |
| `templates/` | **Visão (Frontend)** | Arquivos HTML dinâmicos utilizando o motor **Jinja2**. Inclui o layout mestre (`base.html`), listagem (`events.html`), formulário em Tailwind CSS (`new_event.html`), detalhes (`event_detail.html`) e auditoria (`cia_audit.html`). |
| `requirements.txt` | **Infraestrutura** | Declara todas as bibliotecas do projeto (ex.: `fastapi`, `uvicorn`, `pydantic`, `jinja2`, `python-multipart`), garantindo a reprodutibilidade do ambiente. |

---

## 📁 Estrutura de Pastas do Repositório

```text
FastAPI-Eventos/
├── data/
│   └── db.py               # Camada de persistência em memória
├── models/
│   ├── events.py           # Modelos Pydantic para validação e response_model
│   └── users.py            # Schemas Pydantic para usuários e organizadores
├── router/
│   └── events.py           # Roteamento de rotas JSON e rotas da interface UI
├── templates/
│   ├── base.html           # Template mestre com layout e Tailwind CSS
│   ├── cia_audit.html      # Página do relatório de auditoria da Tríade CIA
│   ├── event_detail.html   # Detalhes do evento
│   ├── events.html         # Listagem de eventos cadastrados
│   └── new_event.html      # Formulário estilizado para novos eventos
├── venv/                   # Ambiente virtual Python isolado
├── main.py                 # Ponto de entrada da aplicação
├── README.md               # Documentação técnica do projeto
└── requirements.txt        # Registro de dependências do projeto



---

## 📝 Resumo dos Exercícios do TP1

### Exercício 1: Ambiente Isolado e Servidor Mínimo

* **Execução:** Criação do ambiente virtual com `virtualenv venv` e instalação do `fastapi` e `uvicorn`.
* **Resultado:** Ponto de entrada em `main.py` com o endpoint `GET /` retornando `{"status": "API operacional"}`.

### Exercício 2: Arquitetura Modular com `APIRouter`

* **Execução:** As rotas do domínio foram concentradas em `router/events.py` e registradas no `main.py` via `include_router`.
* **Justificativa:** Separar rotas por recurso impede que o arquivo principal se torne monolítico, garantindo manutenibilidade e permitindo que a equipe desenvolva novos domínios em paralelo sem sobreposição de código.

### Exercício 3: Prevenção de Vazamento com `response_model`

* **Execução:** Construção do schema `EventoPublico` em `models/events.py` para filtrar retornos públicos.
* **Impacto de Segurança:** A versão sem `response_model` exporia campos internos como `organizador_internal_id` e `audit_token`, facilitando ataques de enumeração de recursos e sequestro de sessão por atores maliciosos.

### Exercício 4: Organização Modular por Responsabilidade

* **Execução:** Divisão clara do projeto nos pacotes `data/`, `models/`, `router/` e `templates/`, estabelecendo fronteiras nítidas para rápida ambientação de novos desenvolvedores.

### Exercício 5: Renderização Dinâmica com Jinja2

* **Execução:** Adição de rotas HTML e templates dinâmicos exibindo nome, data, local e organizador dos eventos sem interferir na rota da API REST JSON (`GET /events`).

### Exercício 6: Mitigação XSS e Herança de Templates

* **Sanitização XSS:** O **auto-escaping** nativo do Jinja2 converte caracteres especiais de tags maliciosas (como `<script>`) em entidades HTML (`&lt;script&gt;`), prevenindo execução de JavaScript no navegador do usuário.
* **Herança:** Utilização de `base.html` como layout base com reutilização de cabeçalho e rodapé em `events.html`, `event_detail.html` e `new_event.html`.

---

## 🖥️ Interface de Usuário (UI)

Além dos endpoints RESTful, a aplicação conta com uma interface Web acessível via navegador:

* **`/event/ui`**: Painel principal para listagem de todos os eventos cadastrados.
* **`/event/ui/new`**: Formulário interativo estilizado com **Tailwind CSS** para cadastro de novos eventos sem necessidade de depender do Swagger.
* **`/event/ui/audit`**: Relatório de Auditoria de Segurança focado nos pilares CIA (Confidencialidade, Integridade e Disponibilidade).

---

## 📊 Exercício 7: Avaliação pela Tríade CIA

| Pilar | Situação Atual | Lacuna Real Observável no Código |
| --- | --- | --- |
| **Confidencialidade** | Ocultação de `audit_token` e IDs internos via `response_model` no Pydantic. | Ausência de controle de acesso e autenticação (JWT/OAuth2) nas rotas públicas. |
| **Integridade** | Validação de tipos e dados obrigatórios via Pydantic em `models/events.py`. | Inexistência de controle de permissões por usuário (RBAC) no banco em memória. |
| **Disponibilidade** | Servidor FastAPI executado sobre arquitetura assíncrona com Uvicorn. | Ausência de camada de Rate Limiting (Redis) para conter requisições massivas. |

---

## 🔒 Arquitetura de Segurança e Modelagem de Ameaças (Exercício 8)

### Diagrama de Fluxo de Dados (DFD)

```text
       [ Usuário / Navegador / Cliente HTTP ] (Não Confiável)
                          │
                          │ (Entrada: Formulário / Payload JSON)
    ======================│====================================== [ Trust Boundary 1: Rede / Entrada ]
                          ▼
           +------------------------------+
           | 1.0 Interface / Formulário   |
           |     (Jinja2 / Form Data)     |
           +------------------------------+
                          │
                          │ (Parâmetros de Entrada)
                          ▼
           +------------------------------+
           | 2.0 Validação e Parsing      |
           |     (FastAPI / Pydantic)     |
           +------------------------------+
                          │
    ======================│====================================== [ Trust Boundary 2: Persistência ]
                          ▼
           +------------------------------+
           | D1  Banco de Dados /         |
           |     Memória (data/db.py)     |
           +------------------------------+

```

* **Trust Boundary 1 (TB1):** Separa requisições externas não confiáveis da camada interna do FastAPI.
* **Trust Boundary 2 (TB2):** Separa a validação de regras de negócio da camada de armazenamento em memória (`data/db.py`).
* **Fluxo de Dados Sensível:** O parâmetro **`organizer`** (assim como `location` e `date`), vindo da **TB1** pelo formulário `POST /event/ui/new`, é sanitizado e validado via Pydantic (Processo 2.0) antes de atingir a **TB2**.

### Tabela de Mapeamento dos Frameworks de Segurança

| Framework | Foco do Framework | Controle de Segurança Concreto | Aplicação no `eventos-api` |
| --- | --- | --- | --- |
| **OWASP** *(Top 10)* | Mitigação de vulnerabilidades Web | **Escape Automático no Jinja2** | O Jinja2 realiza o escape automático de HTML na renderização de variáveis (`{{ event.organizer }}`), prevenindo **Cross-Site Scripting (XSS)**. |
| **NIST SSDF** *(SP 800-218)* | Desenvolvimento seguro e ambiente | **Isolamento de Ambiente (`venv`)** | Uso de ambiente virtual isolado para gerenciamento de dependências, prevenindo contaminação por pacotes vulneráveis do SO. |
| **MITRE ATT&CK** | Mapeamento de táticas e técnicas | **`response_model` no FastAPI** | Garante que os retornos da API limitem a exposição de dados estritamente ao esquema do Pydantic, mitigando **Data Exposure (T1592)**. |

---

## 🚀 Como Executar o Projeto

1. **Ative o ambiente virtual:**
```bash
source venv/bin/activate    # Linux/macOS
# .\venv\Scripts\activate   # Windows

```


2. **Instale as dependências:**
```bash
pip install -r requirements.txt

```


3. **Inicie o servidor Uvicorn:**
```bash
uvicorn main:app --reload

```


4. **Acesse as interfaces e rotas:**
* **Painel Web (Interface UI):** `http://127.0.0.1:8000/event/ui`
* **Formulário de Cadastro:** `http://127.0.0.1:8000/event/ui/new`
* **Relatório de Auditoria CIA:** `http://127.0.0.1:8000/event/ui/audit`
* **Documentação Swagger (OpenAPI):** `http://127.0.0.1:8000/docs`



```

