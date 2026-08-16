# 📅 FastAPI Eventos API

API RESTful desenvolvida com **FastAPI** e **Pydantic** para gerenciamento de eventos e tarefas. O projeto contempla operações completas de CRUD, validação de dados em tempo de execução e geração automática de documentação OpenAPI/Swagger.

---

## 🛠️ Arquitetura e Módulos do Projeto

| Arquivo / Diretório | Camada | Responsabilidade principal |
| :--- | :--- | :--- |
| `main.py` | **Aplicação** | Ponto de entrada (`entrypoint`). Instancia o `FastAPI()`, configura os middlewares, inclui as rotas registradas nos roteadores (`APIRouter`) e define endpoints globais como o status do serviço. |
| `data/db.py` | **Persistência** | Responsável pelo armazenamento e gerenciamento do estado dos dados. Mantém as coleções em memória (listas Python) e abstrai a manipulação de leitura e escrita da camada de roteamento. |
| `models/events.py` | **Domínio / Validação** | Define os esquemas de dados utilizando **Pydantic (`BaseModel`)**. Garante a tipagem estrita dos campos do evento, define valores padrão, campos opcionais e documenta exemplos para o Swagger via `Config`. |
| `router/events.py` | **Controlador (API)** | Contém as definições das rotas HTTP (`GET`, `POST`, `PUT`, `DELETE`). Trata os parâmetros de requisição, aplica códigos de status HTTP apropriados (`200`, `201`, `404`, `422`), gerencia exceções com `HTTPException` e controla a filtragem de saída com `response_model`. |
| `requirements.txt` | **Infraestrutura** | Declara todas as bibliotecas e dependências externas necessárias para a execução do projeto (ex.: `fastapi`, `uvicorn`, `pydantic`), garantindo a reprodutibilidade do ambiente de desenvolvimento. |

---

## 🚀 Como Executar o Projeto

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt