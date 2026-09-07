# 🛡️ Teste de Performance 2 (TP2) — Desenvolvimento Seguro de Aplicações Web

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OAuth2](https://img.shields.io/badge/OAuth2-EB5424?style=for-the-badge&logo=auth0&logoColor=white)](https://oauth.net/2/)
[![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)](https://jwt.io/)

> **Navegação:** ⬅️ [Voltar ao README Principal](../../README.md)

---

## 👨‍💻 Informações do Projeto

* **Disciplina:** Desenvolvimento Seguro de Aplicações Web
* **Estudante:** Weslley Wallace Castro Soares
* **Professor:** Fabiano Domingues
* **Projeto Base:** `eventos-api` (Evolução a partir do TP1)

---

## 📌 Sumário
1. [Visão Geral](#-visão-geral)
2. [Exercício 1 — Misuse Cases](#-exercício-1--misuse-cases)
3. [Exercício 2 — Categorização STRIDE](#-exercício-2--categorização-stride)
4. [Exercício 3 — Threat Model Unificado](#-exercício-3--threat-model-unificado)
5. [Exercício 4 — Fronteiras de Segurança & DFD](#-exercício-4--fronteiras-de-segurança--dfd)
6. [Exercício 5 — Análise de APIs pelos 3 Eixos](#-exercício-5--análise-de-apis-pelos-3-eixos)
7. [Exercício 6 — Autenticação OAuth2, Bcrypt & Ownership](#-exercício-6--autenticação-oauth2-bcrypt--ownership)
8. [Exercício 7 — JWT, MFA & Modelo de Autorização Híbrido](#-exercício-7--jwt-mfa--modelo-de-autorização-híbrido)

---

## 🎯 Visão Geral

Este trabalho apresenta a implementação e a modelagem de segurança para o **`eventos-api`**. O objetivo foi identificar lacunas de segurança deixadas na primeira versão (TP1), criar a modelagem de ameaças (Threat Modeling), definir o diagrama de fluxo de dados (DFD) com fronteiras de confiança, e implementar um sistema completo de **Autenticação e Autorização Híbrida (RBAC + Ownership)** com suporte a **MFA** e **OAuth2/JWT**.

---

## ☣️ Exercício 1 — Misuse Cases

Análise do sistema sob a perspectiva de um atacante para identificar comportamentos maliciosos antes da modelagem formal.

| ID | Misuse Case | Ator Malicioso | Vetor de Ataque Concreto (TP1) | Impacto | Severidade |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MC-01** | Operações Não Autorizadas | Atacante Anônimo | Ausência de autenticação nos endpoints `POST`, `PUT` e `DELETE`. | Perda total de integridade dos dados e danos à reputação. | **Crítico** |
| **MC-02** | Negação de Serviço (DoS) | Botnet / Atacante | Dados em listas na RAM (`data/db.py`) sem limitação de payload ou Rate Limit. | Exaustão de RAM (Out of Memory) e queda do serviço Uvicorn/FastAPI. | **Alto** |
| **MC-03** | Stored XSS via Formulários | Usuário Malicioso | Entrada livre nos campos sem sanitização estrita no Pydantic. | Injeção de scripts no navegador do usuário ao visualizar o evento. | **Médio-Alto** |
| **MC-04** | Raspagem Massiva (Scraping) | Competidor / Scraper | Identificadores numéricos sequenciais e endpoints `GET` abertos. | Quebra de confidencialidade comercial pela extração em massa. | **Médio** |

---

## 🛡️ Exercício 2 — Categorização STRIDE

Mapeamento de ameaças nos componentes estruturais da aplicação utilizando o framework **STRIDE**.

| Componente | Categoria STRIDE | Ameaça Identificada |
| :--- | :--- | :--- |
| **Rotas de Gestão (`router/events.py`)** | **Spoofing** | Publicação de eventos por atacantes anônimos se passando por organizadores legítimos. |
| **Rotas de Gestão (`router/events.py`)** | **Tampering** | Alteração arbitrária de locais, datas e títulos de eventos criados por terceiros. |
| **Persistência na RAM (`data/db.py`)** | **Denial of Service** | Inundação de payloads pesados para provocar crash por estouro de memória. |
| **Persistência na RAM (`data/db.py`)** | **Repudiation** | Falta de logs de auditoria impedindo a rastreabilidade e responsabilização de ações. |
| **Modelos Pydantic (`models/events.py`)** | **Information Disclosure** | Exposição inadvertida de atributos sensíveis e tokens privados no retorno JSON. |
| **Camada de Autenticação / Autorização** | **Elevation of Privilege** | Usuário comum alterando/deletando eventos de terceiros por falta de validação de *ownership*. |
| **Interface Web (`templates/`)** | **Tampering** | Injeção de scripts maliciosos (Stored XSS) nos campos de formulários da interface. |

---

## 📋 Exercício 3 — Threat Model Unificado

Mapeamento completo conectando Ativos, Superfície de Ataque, STRIDE e Mitigações Técnicas.

### 🔑 Ativos Críticos Mapeados
* **AST-01 (Crítico):** Credenciais (Hashes Bcrypt) e Tokens JWT.
* **AST-02 (Alto):** Dados de Eventos armazenados em memória.
* **AST-03 (Alto):** Disponibilidade do Servidor e da API.
* **AST-04 (Médio):** Integridade da Interface Web (UI Jinja2).

---

## 📐 Exercício 4 — Fronteiras de Segurança & DFD

O sistema foi particionado em 3 zonas de confiança para delimitar os pontos de controle:

1. **Partição 1 (Cliente Externo):** Navegadores, cURL e aplicações móveis *(Ambiente Não Confiável)*.
2. **Partição 2 (Camada de Aplicação & API):** FastAPI, Pydantic, Jinja2 e JWT *(Zona de Processamento)*.
3. **Partição 3 (Armazenamento & Persistência):** Módulo `data/db.py` *(Zona Interna Contida)*.

### 🌉 Cruzamento de Fronteiras de Confiança (Trust Boundaries)
* **TB1 (Internet ➔ API):** Requer interceptação de autenticação JWT e validação estrita de tipos via Pydantic para neutralizar *Spoofing* e *XSS*.
* **TB2 (API ➔ Persistência):** Requer aplicação de checagem de *Ownership* (ID do criador == ID do usuário) e limites de tamanho de payload para mitigar *BOLA* e *DoS*.

---

## 🌐 Exercício 5 — Análise de APIs pelos 3 Eixos de Segurança

| Eixo | Vetor de Ataque Identificado | Situação no Threat Model |
| :--- | :--- | :--- |
| **Design** | Utilização inadequada do fluxo OAuth2 para M2M ou falta de escopos granulares para parceiros. | **Lacuna Nova** (Tratada na arquitetura M2M/Client Credentials). |
| **Implementação** | Falha de Autorização no Nível de Objeto (BOLA / Broken Object Level Authorization). | **Já Coberto** (Mitigado no Exercício 3 e 6 via *ownership check*). |
| **Infraestrutura** | DoS por ausência de Rate Limiting/WAF e exposição direta do servidor Uvicorn. | **Parcialmente Coberto** (Requer API Gateway/Reverse Proxy). |

---

## 🔑 Exercício 6 — Autenticação OAuth2, Bcrypt & Ownership

### Implementações
1. **Hashing de Senha:** Utilização do `passlib` com algoritmo `bcrypt` para garantir armazenamento seguro.
2. **OAuth2 Bearer Token:** Implementação do fluxo de autenticação por token.
3. **Validação de Ownership:** Garantia de que **apenas o organizador dono do evento** (ou um `admin`) possa executar modificações (`PUT`/`DELETE`).

---

## 🛡️ Exercício 7 — JWT, MFA & Modelo de Autorização Híbrido

### Funcionalidades Avançadas
* **Validade de Token:** Expiração configurada via claim `exp` no JWT.
* **MFA para Administradores:** Exigência de segundo fator de autenticação (`mfa_secret`) para usuários do perfil `admin`.
* **Suporte M2M (Machine-to-Machine):** Suporte ao fluxo `client_credentials` com escopos contratuais (ex: `events:sync-inventory`).

### Modelo de Autorização Recomendado: **Híbrido (RBAC + Ownership/ReBAC)**
* **RBAC:** Utilizado para controle geral de acesso às rotas por perfil (`admin`, `organizador`, `participante`).
* **Ownership (Por Recurso):** Utilizado na camada de objeto para garantir isolamento de dados entre organizadores.

---

## 🛠️ Como Executar o Projeto

```bash
# 1. Clonar o repositório
git clone <url-do-repositorio>

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Executar o servidor FastAPI
uvicorn main:app --reload

# 4. Acessar a documentação interativa
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)