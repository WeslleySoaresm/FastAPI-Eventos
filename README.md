
```markdown
# 📅 FastAPI Eventos API

API RESTful desenvolvida com **FastAPI** e **Pydantic** para gerenciamento de eventos e tarefas. O projeto contempla operações completas de CRUD, validação de dados em tempo de execução, interface web interativa renderizada com **Jinja2** e **Tailwind CSS**, além de documentação automática OpenAPI/Swagger.

---

## 🛠️ Arquitetura e Módulos do Projeto

| Arquivo / Diretório | Camada | Responsabilidade principal |
| :--- | :--- | :--- |
| `main.py` | **Aplicação** | Ponto de entrada (`entrypoint`). Instancia o `FastAPI()`, configura os middlewares, inclui as rotas registradas nos roteadores (`APIRouter`) e define endpoints globais como o status do serviço. |
| `data/db.py` | **Persistência** | Responsável pelo armazenamento e gerenciamento do estado dos dados. Mantém as coleções em memória (listas Python) e abstrai a manipulação de leitura e escrita da camada de roteamento. |
| `models/events.py` | **Domínio / Validação** | Define os esquemas de dados utilizando **Pydantic (`BaseModel`)**. Garante a tipagem estrita dos campos do evento, define valores padrão, campos opcionais e documenta exemplos para o Swagger via `Config`. |
| `router/events.py` | **Controlador (API & UI)** | Contém as definições das rotas HTTP (`GET`, `POST`, `PUT`, `DELETE`) para a API REST e as rotas HTML (`/ui`, `/ui/new`, `/ui/{id}`). Trata dados de formulário com `Form(...)`, aplica códigos de status HTTP, lida com exceções (`HTTPException`) e redirecionamentos (`RedirectResponse`). |
| `templates/` | **Visão (Frontend)** | Arquivos HTML dinâmicos utilizando o motor de template **Jinja2**. Inclui o layout base (`base.html`), a listagem de eventos (`events.html`), o formulário estilizado com Tailwind CSS (`new_event.html`) e o relatório de auditoria (`cia_audit.html`). |
| `requirements.txt` | **Infraestrutura** | Declara todas as bibliotecas e dependências externas necessárias para a execução do projeto (ex.: `fastapi`, `uvicorn`, `pydantic`, `jinja2`, `python-multipart`), garantindo a reprodutibilidade do ambiente de desenvolvimento. |

---

## 🖥️ Interface de Usuário (UI)

Além dos endpoints RESTful, a aplicação conta com uma interface Web acessível via navegador:

* **`/event/ui`**: Painel principal para listagem de todos os eventos cadastrados.
* **`/event/ui/new`**: Formulário interativo estilizado com **Tailwind CSS** para cadastro de novos eventos sem necessidade de depender do Swagger.
* **`/event/ui/audit`**: Relatório de Auditoria de Segurança focado nos pilares CIA (Confidencialidade, Integridade e Disponibilidade).

---

## 🔒 Arquitetura de Segurança e Modelagem de Ameaças (Exercício 8)

Como parte do alinhamento com a equipe de segurança e modelagem de ameaças, a aplicação conta com um **Diagrama de Fluxo de Dados (DFD)** e mapeamento de frameworks de referência.

### Diagrama de Fluxo de Dados (DFD)
O fluxo de dados da aplicação contempla as fronteiras de confiança (**Trust Boundaries**) para o processamento e armazenamento seguro de dados:

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

* **Trust Boundary 1 (TB1):** Separa os clientes externos e dados enviados via formulário/HTTP da execução interna da aplicação.
* **Trust Boundary 2 (TB2):** Separa a lógica de validação do repositório em memória.
* **Fluxo de Dados Sensível:** O parâmetro **`organizer`** (junto a `location` e `date`), que entra através da **TB1** pelo formulário `POST /event/ui/new`, é sanitizado e validado na camada Pydantic (Processo 2.0) antes de ser gravado na **TB2**.

### Tabela de Mapeamento dos Frameworks de Segurança

| Framework | Foco do Framework | Controle de Segurança Concreto | Aplicação no `eventos-api` |
| --- | --- | --- | --- |
| **OWASP** *(Top 10 / ASVS)* | Mitigação de vulnerabilidades Web | **Escape Automático no Jinja2** | O Jinja2 realiza o escape automático de HTML na renderização das variáveis (`{{ event.organizer }}`), prevenindo **Cross-Site Scripting (XSS)**. |
| **NIST SSDF** *(SP 800-218)* | Desenvolvimento seguro e ambiente | **Isolamento de Ambiente (`venv`)** | Uso de ambiente virtual isolado para gerenciamento de dependências, prevenindo contaminação por pacotes vulneráveis do SO. |
| **MITRE ATT&CK** | Mapeamento de táticas e técnicas | **`response_model` no FastAPI** | Garante que os retornos da API limitem a exposição de dados estritamente ao esquema do Pydantic, mitigando **Data Exposure**. |

---

## 🚀 Como Executar o Projeto

1. **Instale as dependências:**
```bash
pip install -r requirements.txt

```


2. **Inicie o servidor Uvicorn:**
```bash
uvicorn main:app --reload

```


3. **Acesse as interfaces:**
* **Interface Web:** `http://127.0.0.1:8000/event/ui`
* **Novo Evento (Formulário):** `http://127.0.0.1:8000/event/ui/new`
* **Documentação Swagger:** `http://127.0.0.1:8000/docs`



```

```