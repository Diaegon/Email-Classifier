# Email Classifier LLM

Sistema inteligente de classificação de emails para empresas do setor financeiro. Utiliza APIs de LLM (Large Language Models) para classificar emails como **Produtivo** ou **Improdutivo** com base no contexto corporativo, além de oferecer funcionalidades avançadas de consulta de clientes e gerenciamento de banco de dados.

## 🎯 Características

### 🤖 Classificação de Emails
- **Classificação Inteligente**: Usa IA para analisar emails e determinar se são produtivos ou improdutivos
- **Múltiplas APIs**: Suporte para OpenAI, Anthropic Claude, Google Gemini e Ollama
- **Upload de Arquivos**: Suporte para arquivos `.txt` e `.pdf` com botão de limpeza
- **Respostas Sugeridas**: Gera respostas automáticas baseadas na classificação
- **Contexto Empresarial**: Prompt especializado para empresas do setor financeiro

### 👥 Gestão de Clientes
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

### 🗄️ Sistema de Banco de Dados
- **Migrações com Alembic**: Controle de versão do schema
- **Suporte Multi-Banco**: SQLite (dev), PostgreSQL e MySQL (prod)
- **Variáveis de Ambiente**: Configuração flexível por ambiente
- **Context Managers**: Gerenciamento seguro de sessões

## 📁 Estrutura do Projeto

```
email-classifier-llm/
├── apps/
│   ├── backend/                    # API FastAPI
│   │   ├── email_classifier_llm/
│   │   │   ├── models/            # Modelos SQLAlchemy
│   │   │   ├── routers/           # Endpoints da API
│   │   │   ├── services/          # Lógica de negócio
│   │   │   └── database.py        # Configuração do banco
│   │   ├── migrations/            # Migrações Alembic
│   │   ├── alembic.ini           # Configuração Alembic
│   │   ├── migrate.py            # Script de migrações
│   │   └── pyproject.toml        # Dependências Python
│   └── frontend/                   # Interface Web
│       ├── index.html            # Página principal
│       ├── app.js               # JavaScript
│       └── styles.css           # Estilos CSS
├── railway.json                  # Configuração Railway
└── README.md                    # Documentação
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
# Configuração do Banco de Dados
DB_DATABASE_URL=sqlite:///./email_classifier.db

# Escolha uma das opções de LLM:

# Opção 1: OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4o-mini

# Opção 2: Anthropic Claude
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sua_chave_aqui
ANTHROPIC_MODEL=claude-3-haiku-20240307

# Opção 3: Google Gemini
LLM_PROVIDER=google
GOOGLE_API_KEY=sua_chave_aqui
GOOGLE_MODEL=gemini-1.5-flash

# Opção 4: Ollama (local)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

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

**MySQL (Produção):**
```env
DB_DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/email_classifier
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

### Consulta de Clientes

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

## Deploy

### Railway (Recomendado)
1. Conecte seu repositório no [Railway](https://railway.app)
2. Adicione um serviço PostgreSQL:
   - Vá em "New Project" → "Database" → "PostgreSQL"
   - Ou use o `railway.json` já configurado
3. Configure as variáveis de ambiente:
   - `LLM_PROVIDER=google`
   - `GOOGLE_API_KEY=sua_chave_aqui`
   - `GOOGLE_MODEL=gemini-2.0-flash`
   - `DB_DATABASE_URL=${{Postgres.DATABASE_URL}}` (conecta automaticamente ao PostgreSQL)
4. Deploy automático será executado

**⚠️ Importante**: SQLite não funciona em produção no Railway devido ao sistema de arquivos efêmero. Use PostgreSQL ou MySQL.

### Migração para Produção

Se você já tem dados no SQLite local e quer migrar para PostgreSQL:

```bash
# 1. Configure a variável de ambiente com a URL do PostgreSQL
export DB_DATABASE_URL="postgresql://usuario:senha@host:5432/database"

# 2. Execute o script de migração
python migrate_to_production.py
```

O script irá:
- ✅ Conectar ao SQLite local
- ✅ Conectar ao PostgreSQL de produção
- ✅ Migrar todos os clientes
- ✅ Verificar duplicatas
- ✅ Confirmar a migração

### Outras opções
- Backend: Render / Fly.io
- Frontend: já é servido pelo backend. Alternativamente, hospedar `apps/frontend` em Vercel e apontar para a API pública.

## ⚙️ Variáveis de Ambiente

### Banco de Dados
- `DB_DATABASE_URL`: URL do banco de dados (padrão: SQLite)

### LLM Providers
- `LLM_PROVIDER`: `openai`, `anthropic`, `google`, `ollama`
- `OPENAI_API_KEY`: chave da OpenAI (se `LLM_PROVIDER=openai`)
- `OPENAI_MODEL`: modelo da OpenAI (padrão `gpt-4o-mini`)
- `ANTHROPIC_API_KEY`: chave da Anthropic (se `LLM_PROVIDER=anthropic`)
- `ANTHROPIC_MODEL`: modelo da Anthropic (padrão `claude-3-haiku-20240307`)
- `GOOGLE_API_KEY`: chave do Google (se `LLM_PROVIDER=google`)
- `GOOGLE_MODEL`: modelo do Google (padrão `gemini-1.5-flash`)
- `OLLAMA_BASE_URL`: URL do Ollama (se `LLM_PROVIDER=ollama`)
- `OLLAMA_MODEL`: modelo do Ollama (padrão `llama3.2`)

## 🚀 Funcionalidades Principais

### Interface Web
- **Layout Responsivo**: 70% classificação de emails, 30% consulta de clientes
- **Upload de Arquivos**: Suporte para `.txt` e `.pdf` com botão de limpeza
- **Resposta Editável**: Área para editar e copiar respostas da IA
- **Busca em Tempo Real**: Consulta de clientes com resultados instantâneos
- **Feedback Visual**: Animações e confirmações para melhor UX

### Sistema de Banco de Dados
- **Modelo de Clientes**: Nome, CPF, data de nascimento, perfil de investidor, ativos custodiados
- **Migrações Alembic**: Controle de versão do schema
- **Context Managers**: Gerenciamento seguro de sessões
- **Suporte Multi-Banco**: SQLite, PostgreSQL, MySQL

### APIs de IA
- **Múltiplas APIs**: OpenAI, Anthropic, Google Gemini, Ollama
- **Classificação Inteligente**: Produtivo vs Improdutivo
- **Respostas Sugeridas**: Geração automática de respostas
- **Contexto Empresarial**: Prompts especializados para setor financeiro
