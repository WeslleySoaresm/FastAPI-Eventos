# README2.md: Relatório Técnico Detalhado — TP3 (Desenvolvimento Seguro de Aplicações Web)

Este documento apresenta a descrição detalhada de todas as etapas, vulnerabilidades tratadas e decisões arquiteturais implementadas no projeto **eventos-api** durante o Teste de Performance 3 (TP3).

---

## 📑 Índice dos Exercícios

1. [Exercício 1: Prevenção de SQL Injection com Whitelist e Regex](https://www.google.com/search?q=%23exerc%C3%ADcio-1)
2. [Exercício 2: Análise Crítica de Vulnerabilidades (OWASP Top 10)](https://www.google.com/search?q=%23exerc%C3%ADcio-2)
3. [Exercício 3: Mapeamento de Falha BOLA / IDOR](https://www.google.com/search?q=%23exerc%C3%ADcio-3)
4. [Exercício 4: Correção Centralizada e Validação de Payload (`extra=forbid`)](https://www.google.com/search?q=%23exerc%C3%ADcio-4)
5. [Exercício 5: Mitigação de Stored XSS com Output Encoding](https://www.google.com/search?q=%23exerc%C3%ADcio-5)
6. [Exercício 6: Configuração de CORS e Cabeçalhos de Segurança HTTP](https://www.google.com/search?q=%23exerc%C3%ADcio-6)
7. [Exercício 7: Rate Limiting Diferenciado para Proteção de Rotas Sensíveis](https://www.google.com/search?q=%23exerc%C3%ADcio-7)
8. [Exercício 8: Migração de Persistência para PostgreSQL com SQLModel e BaseSettings](https://www.google.com/search?q=%23exerc%C3%ADcio-8)

---

### 1. Prevenção de SQL Injection (Exercício 1)

* **Problema:** O endpoint de busca de eventos concatenava diretamente os parâmetros do usuário na query, permitindo manipulação indevida (ex: injeção de cláusulas SQL como `' OR '1'='1`).
* **Solução Implementada:**
* Aplicação de validação estricta baseada em Regex e Whitelist (`re.match`) no parâmetro de busca.
* Rejeição imediata de entradas contendo caracteres especiais ou vetores de ataque com código de status `422 Unprocessable Entity`.
* Utilização de parâmetros vinculados (query parameters seguros) no ORM.



### 2. Análise Crítica OWASP Top 10 (Exercício 2)

Realizou-se a leitura crítica de trechos de código para mapear três categorias do OWASP Top 10:

* **A01:2021 – Broken Access Control (BOLA):** Ausência de verificação de propriedade (`ownership`) ao atualizar recursos por ID na URL.
* **A02/A07 – Cryptographic / Authentication Failures:** Uso de segredos e chaves de criptografia (`SECRET_KEY`) hardcoded no código-fonte.
* **A05:2021 – Security Misconfiguration:** Dependência de listas globais em memória para persistência, inviabilizando ambientes concorrentes e seguros de produção.

### 3. Mapeamento de Falha BOLA / IDOR (Exercício 3)

* **Cenário Analisado:** O endpoint `GET /inscricoes/{id}` permitia que um usuário autenticado acessasse os dados de inscrição de outra pessoa apenas alterando o ID numérico sequencial na URL.
* **Identificação:** Falta de validação comparando o `user_id` do registro recuperado com o identificador extraído do token JWT (`current_user["id"]`).

### 4. Correção Centralizada e Validação de Payload (Exercício 4)

* **Middleware JWT:** Centralização da validação de token e checagem de propriedade de recursos antes de atingir as rotas sensíveis.
* **Validação Rígida (Pydantic):** Configuração dos modelos com `model_config = SettingsConfigDict(extra="forbid")` para rejeitar automaticamente campos extras não documentados enviados nas requisições.

### 5. Mitigação de Stored XSS (Exercício 5)

* **Problema:** Injeção de scripts maliciosos em comentários exibidos na página de detalhes do evento.
* **Solução:** Ativação do escape automático (`autoescape`) nativo do motor de templates Jinja2, garantindo que qualquer código HTML/JavaScript inserido seja renderizado como texto literal inofensivo.

### 6. CORS e Cabeçalhos de Segurança HTTP (Exercício 6)

* **CORSMiddleware:** Restrição de origens permitidas via allowlist explícita (proibido o uso de wildcard `*`).
* **Cabeçalhos Defensivos:** Adição de middlewares para injeção automática de cabeçalhos essenciais:
* `Strict-Transport-Security` (HSTS)
* `X-Frame-Options`
* `X-Content-Type-Options`



### 7. Rate Limiting Diferenciado (Exercício 7)

* **Proteção contra Força Bruta:** Aplicação de limites de requisições restritos e específicos para rotas críticas (como login e criação de contas), diferenciando-os do tráfego comum de listagem para não prejudicar a experiência de usuários legítimos.

### 8. Migração para PostgreSQL com SQLModel e BaseSettings (Exercício 8)

* **Persistência Relacional:** Substituição definitiva da estrutura em memória pelo PostgreSQL, com modelos `User` e `Event` estruturados via SQLModel.
* **Injeção de Sessão:** Gerenciamento do ciclo de vida das conexões via `Depends(get_session)`.
* **Gestão de Segredos:** Configuração do `pydantic-settings` (`BaseSettings`) integrado a um arquivo `.env` seguro e ignorado pelo controle de versão.

---

## 🔙 Navegação

* [Voltar para o README 1 (TP1)](https://www.google.com/search?q=./README01.md)