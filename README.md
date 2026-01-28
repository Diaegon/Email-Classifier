# Email Classifier LLM

Sistema inteligente de classificação de emails para empresas do setor financeiro. Utiliza APIs de LLM (Large Language Models) para classificar emails como **Produtivo** ou **Improdutivo** com base no contexto corporativo, além de oferecer funcionalidades avançadas de consulta de clientes e gerenciamento de banco de dados.

## 🎯 Características

### 🤖 Classificação de Emails
- **Classificação Inteligente**: Usa IA para analisar emails e determinar se são produtivos ou improdutivos de acordo com um contexto
- **Múltiplas APIs**: Refatorado para utilizar a API do google gemini, porém a modularização facilita uma troca para outra API de sua preferência
- **Upload de Arquivos**: Suporte para arquivos `.txt` e `.pdf` com botão de limpeza
- **Respostas Sugeridas**: Gera respostas automáticas baseadas na classificação
- **Contexto Empresarial**: Prompt especializado para empresas do setor financeiro, mas pode ser facilmente alterado para outro tipo de contexto.

### 👥 Gestão de Clientes (em desenvolvimento)
- **Banco de Dados SQLite**: Sistema completo de persistência de dados
- **Busca Inteligente**: Pesquisa por nome, CPF, número do cliente ou email
- **Dados Completos**: Nome, CPF, data de nascimento, perfil de investidor, ativos custodiados
- **Status de Pagamento**: Controle de plano contratual em dia/atraso
- **Interface Integrada**: Consulta de clientes ao lado da classificação de emails

### 🎨 Interface Moderna
- **Layout Responsivo**: 70% classificação de emails, 30% consulta de clientes
- **Paleta de Cores Azul**: Design consistente e profissional
- **Resposta Editável**: Área para editar e copiar respostas da IA
- **Feedback Visual**: Animações e confirmações para melhor UX
- **Busca em Tempo Real**: Resultados instantâneos conforme digitação

### 🗄️ Sistema de Banco de Dados(em desenvolvimento)
- **Migrações com Alembic**: Controle de versão do schema
- **Suporte Multi-Banco**: SQLite (dev), PostgreSQL e MySQL (prod)
- **Variáveis de Ambiente**: Configuração flexível por ambiente
- **Context Managers**: Gerenciamento seguro de sessões

## 📁 Estrutura do Projeto

```
# Documentação

├── apps
│   ├── backend  
│   │   ├── alembic.ini 
│   │   ├── core
│   │   │   ├── config.py #configurações gerais
│   │   │   └── path.py #caminhos utilizados no código
│   │   ├── email_classifier_llm  
│   │   │   ├── database.py  #database (em desenvolvimento)
│   │   │   ├── __init__.py
│   │   │   ├── main.py  #aplicação
│   │   │   ├── models
│   │   │   │   ├── client.py # schemas
│   │   │   │   └── __init__.py
│   │   │   ├── prompts
│   │   │   │   └── prompt_v1.txt #prompt para definir a resposta do modelo.
│   │   │   ├── routers
│   │   │   │   ├── classify.py
│   │   │   │   ├── clients.py
│   │   │   │   └── __init__.py
│   │   │   └── services
│   │   │       ├── client_service.py
│   │   │       ├── __init__.py
│   │   │       ├── llm_client.py
│   │   │       └── processor.py
│   │   ├── migrations
│   │   ├── poetry.lock
│   │   ├── pyproject.toml
│   │   ├── pytest.ini
│   │   ├── README.md
│   │   ├── run_migrations.py
│   │   └── tests
│   │       ├── __init__.py
│   │       └── test_health.py
│   └── frontend
│       ├── app.js
│       ├── index.html
│       └── styles.css
├── docker-compose.yml
├── Dockerfile
└── README.md

```

## Requisitos

- Python 3.13+
- Poetry

## Setup e execução (dev)

1. Entre na pasta do backend e instale dependências:

```bash
cd apps/backend
poetry install
```

2. Configure as variáveis de ambiente no `.env`:

```bash


# Opção 3: Google Gemini
LLM_PROVIDER=google
GOOGLE_API_KEY=sua_chave_aqui
GOOGLE_MODEL=gemini-1.5-flash



3. Rode o servidor:

```bash
poetry run uvicorn email_classifier_llm.main:app --reload --host 0.0.0.0 --port 8000
```

4. Acesse o frontend:

- `http://localhost:8000/` → Interface completa com classificação de emails e consulta de clientes

## 🗄️ Gerenciamento de Banco de Dados

### Migrações com Alembic

```bash
# Inicializar migrações (apenas na primeira vez)
python migrate.py init

# Criar nova migração
python migrate.py create "Descrição da mudança"

# Aplicar migrações
python migrate.py upgrade

# Reverter migração
python migrate.py downgrade -1

# Ver histórico
python migrate.py history
```

### Suporte a Diferentes Bancos

**SQLite (Desenvolvimento):**
```env
DB_DATABASE_URL=sqlite:///./email_classifier.db
```

**PostgreSQL (Produção):**
```env
DB_DATABASE_URL=postgresql://usuario:senha@localhost:5432/email_classifier
```

## 🔌 Uso da API

### Classificação de Emails

`POST /api/classify` (multipart/form-data)

**Campos:**
- `text` (opcional) — texto do email
- `file` (opcional) — arquivo `.txt` ou `.pdf`

**Resposta (JSON):**
```json
{
  "category": "Produtivo" | "Improdutivo",
  "reason": "string",
  "suggested_reply": "string"
}
```

### Consulta de Clientes (desenvolvimento)

`GET /api/clients/search?q=termo` - Busca clientes
`GET /api/clients/{id}` - Cliente específico por ID
`GET /api/clients` - Lista todos os clientes

**Resposta de busca (JSON):**
```json
{
  "success": true,
  "count": 1,
  "clients": [
    {
      "id": 1,
      "nome_completo": "João Silva Santos",
      "cpf": "123.456.789-00",
      "data_nascimento": "1985-03-15",
      "numero_cliente": "CLI001",
      "email": "joao.silva@email.com",
      "perfil_investidor": "Conservador",
      "ativos_custodiados": "Tesouro Selic, CDB, LCI",
      "plano_contratual_em_dia": true
    }
  ]
}
```

## Testes

```bash
cd apps/backend
poetry run pytest -q
```

## Deploy (em produção)

## ⚙️ Variáveis de Ambiente

### Banco de Dados
- `DB_DATABASE_URL`: URL do banco de dados (padrão: SQLite)

### LLM Providers
- `LLM_PROVIDER`: `google`

- `GOOGLE_API_KEY`: chave do Google (se `LLM_PROVIDER=google`)
- `GOOGLE_MODEL`: modelo do Google (padrão `gemini-1.5-flash`)


## 🚀 Funcionalidades Principais

### Interface Web
- **Layout Responsivo**: 70% classificação de emails, 30% consulta de clientes
- **Upload de Arquivos**: Suporte para `.txt` e `.pdf` com botão de limpeza
- **Resposta Editável**: Área para editar e copiar respostas da IA
- **Busca em Tempo Real**: Consulta de clientes com resultados instantâneos (em produção)
- **Feedback Visual**: Animações e confirmações para melhor UX

### Sistema de Banco de Dados
- **Modelo de Clientes**: Nome, CPF, data de nascimento, perfil de investidor, ativos custodiados
- **Migrações Alembic**: Controle de versão do schema
- **Context Managers**: Gerenciamento seguro de sessões
- **Suporte Multi-Banco**: SQLite, PostgreSQL, MySQL

### APIs de IA
- **Múltiplas APIs**: Google Gemini
- **Classificação Inteligente**: Produtivo vs Improdutivo
- **Respostas Sugeridas**: Geração automática de respostas
- **Contexto Empresarial**: Prompts especializados para setor financeiro
