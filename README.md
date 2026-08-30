
# 📅 FastAPI Eventos API (`FastAPI-Eventos`)

![FastAPI](https://img.shields.io/badge/FastAPI-005587?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Security](https://img.shields.io/badge/Security-OWASP_|_NIST_|_MITRE-red?style=for-the-badge)

**Disciplina:** Arquitetura e Segurança de APIs REST com FastAPI — TP1  
**Repositório:** `FastAPI-Eventos`

API RESTful e aplicação web desenvolvida com **FastAPI** e **Pydantic** para gerenciamento de eventos. O projeto contempla operações completas de CRUD, validação de dados em tempo de execução, controle de exposição de dados sensíveis, interface web interativa renderizada com **Jinja2** e **Tailwind CSS**, além de arquitetura de segurança alinhada aos frameworks **OWASP**, **NIST SSDF** e **MITRE ATT&CK**.

---

## 📌 Sumário
- [🚀 Como Executar o Projeto](#-como-executar-o-projeto)
- [🖥️ Interface de Usuário (UI)](#️-interface-de-usuário-ui)
- [🛠️ Arquitetura e Módulos do Projeto](#️-arquitetura-e-módulos-do-projeto)
- [📁 Estrutura de Pastas](#-estrutura-de-pastas)
- [📝 Resumo dos Exercícios do TP1](#-resumo-dos-exercícios-do-tp1)
- [📊 Avaliação pela Tríade CIA (Exercício 7)](#-avaliação-pela-tríade-cia-exercício-7)
- [🔒 Segurança e Modelagem de Ameaças (Exercício 8)](#-segurança-e-modelagem-de-ameaças-exercício-8)

---

## 🚀 Como Executar o Projeto

### Pró-requisitos
Certifique-se de ter o **Python 3.10+** instalado em sua máquina.

### Passos para execução

1. **Clone o repositório e acesse a pasta:**
   ```bash
   git clone <url-do-repositorio>
   cd FastAPI-Eventos

```

2. **Crie e ative o ambiente virtual:**
* **Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate

```


* **Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate

```




3. **Instale as dependências:**
```bash
pip install -r requirements.txt

```


4. **Inicie o servidor Uvicorn:**
```bash
uvicorn main:app --reload

```


5. **Acesse as rotas no navegador:**
* 🎨 **Painel Web (Listagem UI):** [http://127.0.0.1:8000/event/ui](http://127.0.0.1:8000/event/ui)
* 📝 **Formulário de Cadastro:** [http://127.0.0.1:8000/event/ui/new](http://127.0.0.1:8000/event/ui/new)
* 🛡️ **Relatório de Auditoria CIA:** [http://127.0.0.1:8000/event/ui/audit](http://127.0.0.1:8000/event/ui/audit)
* 📖 **Documentação Interativa (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)



---

## 🖥️ Interface de Usuário (UI)

A aplicação vai além da API JSON e disponibiliza uma interface Web amigável e estilizada:

* **`/event/ui`**: Painel principal para visualização dinâmica de todos os eventos cadastrados.
* **`/event/ui/new`**: Formulário interativo estilizado com **Tailwind CSS** para cadastro direto de eventos sem necessidade da interface do Swagger.
* **`/event/ui/audit`**: Dashboard interativo exibindo o relatório de Auditoria de Segurança focado nos pilares da Tríade CIA.

---

## 🛠️ Arquitetura e Módulos do Projeto

A aplicação adota uma arquitetura em camadas clara e desacoplada:

| Camada | Arquivo / Diretório | Responsabilidade Principal |
| --- | --- | --- |
| **Ponto de Entrada** | `main.py` | Instancia o `FastAPI()`, inclui roteadores (`APIRouter`) e expõe endpoints globais de *healthcheck* (`GET /`). |
| **Persistência** | `data/db.py` | Mantém o estado dos dados em memória (listas Python) e abstrai as operações de leitura e escrita. |
| **Domínio / Validação** | `models/events.py`<br>

<br>`models/users.py` | Esquemas **Pydantic (`BaseModel`)** com tipagem estrita, sanitização de campos e filtro de resposta (`response_model`). |
| **Controlador** | `router/events.py` | Gerencia rotas RESTful JSON (`GET`, `POST`, `PUT`, `DELETE`) e rotas Web HTML (`/event/ui`), tratando formulários (`Form`) e exceções (`HTTPException`). |
| **Visão (Frontend)** | `templates/` | Templates HTML dinâmicos em **Jinja2** com estilização **Tailwind CSS** e uso de herança de layout (`base.html`). |
| **Infraestrutura** | `requirements.txt` | Mapeia todas as dependências do ecossistema do projeto (`fastapi`, `uvicorn`, `pydantic`, `jinja2`, etc.). |

---

## 📁 Estrutura de Pastas

```text
FastAPI-Eventos/
├── data/
│   └── db.py               # Camada de persistência em memória
├── models/
│   ├── events.py           # Modelos Pydantic para validação e response_model
│   └── users.py            # Schemas Pydantic para usuários e organizadores
├── router/
│   └── events.py           # Roteamento de endpoints JSON REST e rotas UI HTML
├── templates/
│   ├── base.html           # Template mestre (Layout global com Tailwind CSS)
│   ├── cia_audit.html      # Página do relatório de auditoria da Tríade CIA
│   ├── event_detail.html   # Visualização detalhada do evento
│   ├── events.html         # Painel de listagem de eventos
│   └── new_event.html      # Formulário interativo de cadastro
├── venv/                   # Ambiente virtual Python isolado
├── main.py                 # Ponto de entrada da aplicação FastAPI
├── README.md               # Documentação técnica e guia do projeto
└── requirements.txt        # Registro de dependências externas

```

---

## 📝 Resumo dos Exercícios do TP1

### 🔹 Exercício 1: Ambiente Isolado e Servidor Mínimo

* **Execução:** Configuração do ambiente virtual (`venv`) e instalação dos pacotes base `fastapi` e `uvicorn`.
* **Resultado:** Endpoint básico `GET /` em `main.py` validando o status da API.

### 🔹 Exercício 2: Arquitetura Modular com `APIRouter`

* **Execução:** Isolamento das rotas de domínio dentro do módulo `router/events.py`.
* **Justificativa:** Previne a criação de um arquivo principal monolítico, simplificando a manutenção e permitindo que múltiplos desenvolvedores atuem em módulos distintos simultaneamente sem gerar conflitos no Git.

### 🔹 Exercício 3: Prevenção de Vazamento com `response_model`

* **Execução:** Implementação do esquema Pydantic `EventoPublico` para filtragem automatizada dos dados retornados na API.

> ⚠️ **Impacto de Segurança:** A ausência do `response_model` expõe atributos internos e sensíveis, como `organizador_internal_id` e `audit_token`, facilitando cenários de enumeração de recursos e sequestro de tokens por atacantes.

### 🔹 Exercício 4: Organização Modular por Responsabilidade

* **Execução:** Separação estrita do projeto nos pacotes `data/`, `models/`, `router/` e `templates/`, facilitando o *onboarding* de novos membros na equipe.

### 🔹 Exercício 5: Renderização Dinâmica com Jinja2

* **Execução:** Criação de rotas HTML utilizando `Jinja2Templates` para servir páginas dinâmicas contendo os dados dos eventos sem impactar as rotas da API REST.

### 🔹 Exercício 6: Mitigação XSS e Herança de Templates

* **Sanitização XSS:** Aproveita o **auto-escaping** padrão do Jinja2 para converter caracteres de *scripts* maliciosos (como `<script>`) em entidades HTML seguras (`&lt;script&gt;`).
* **Herança:** Centralização do layout mestre em `base.html`, herdado pelas telas secundárias através da diretiva `{% extends "base.html" %}`.

---

## 📊 Avaliação pela Tríade CIA (Exercício 7)

| Pilar | Situação Atual | Lacuna Real Observável no Código |
| --- | --- | --- |
| **Confidencialidade** | Ocultação de `audit_token` e IDs internos no JSON público via `response_model`. | Ausência de autenticação e autorização (ex.: JWT, OAuth2); qualquer cliente pode consultar os endpoints. |
| **Integridade** | Validação de tipos, presença de campos obrigatorios e regras de schema via Pydantic. | Falta de controle de acesso baseado em papéis (RBAC), permitindo modificações indiscriminadas no banco em memória. |
| **Disponibilidade** | Arquitetura assíncrona orientada a alta performance com FastAPI + Uvicorn. | Inexistência de um middleware de *Rate Limiting* (ex.: Redis/slowapi) para contenção de ataques DoS/brute-force. |

---

## 🔒 Segurança e Modelagem de Ameaças (Exercício 8)

### Diagrama de Fluxo de Dados (DFD)

O diagrama abaixo ilustra as **Fronteiras de Confiança (Trust Boundaries)** da aplicação durante o ciclo de processamento da informação:

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

* **Trust Boundary 1 (TB1):** Limite entre a rede externa/clientes não confiáveis e os manipuladores de rotas internos do FastAPI.
* **Trust Boundary 2 (TB2):** Limite entre as regras de validação/negócio e o banco de dados em memória (`data/db.py`).
* **Fluxo Sensível:** Os dados de formulário enviados via `POST /event/ui/new` passam obrigatoriamente pela validação e sanitização do Pydantic (Processo 2.0) na **TB1** antes de serem persistidos na **TB2**.

### Tabela de Mapeamento dos Frameworks de Segurança

| Framework | Foco do Framework | Controle Concreto Aplicado | Aplicação Prática no Projeto |
| --- | --- | --- | --- |
| **OWASP** *(Top 10)* | Mitigação de falhas e vulnerabilidades Web | **Escape Automático no Jinja2** | Neutralização automatizada de vetores de **Cross-Site Scripting (XSS)** na renderização das variáveis em tela (`{{ event.organizer }}`). |
| **NIST SSDF** *(SP 800-218)* | Segurança no ciclo de vida de software | **Isolamento via `venv**` | Proteção da cadeia de suprimentos garantindo dependências isoladas e reproduzíveis, evitando a contaminação do ambiente operacional. |
| **MITRE ATT&CK** | Mapeamento de técnicas de ataque | **Filtro `response_model**` | Dificulta a fase de **Reconnaissance / Exposição de Dados (T1592)** ao omitir dados e tokens internos nas respostas REST. |

```

