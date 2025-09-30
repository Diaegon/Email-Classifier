# Email Classifier

Sistema inteligente de classificação de emails para empresas do setor financeiro. Utiliza APIs de LLM (Large Language Models) para classificar emails como **Produtivo** ou **Improdutivo** com base no contexto corporativo.

## 🎯 Características

- **Classificação Inteligente**: Usa IA para analisar emails e determinar se são produtivos ou improdutivos
- **Múltiplas APIs**: Suporte para OpenAI, Anthropic Claude, Google Gemini e Ollama
- **Interface Web**: Frontend intuitivo para classificação de emails
- **Upload de Arquivos**: Suporte para arquivos `.txt` e `.pdf`
- **Respostas Sugeridas**: Gera respostas automáticas baseadas na classificação
- **Contexto Empresarial**: Prompt especializado para empresas do setor financeiro

## Estrutura

- `apps/backend`: API FastAPI com integração LLM
- `apps/frontend`: Frontend estático (HTML/CSS/JS) servido pelo FastAPI

## Requisitos

- Python 3.13+
- Poetry

## Setup e execução (dev)

1. Entre na pasta do backend e instale dependências:

```bash
cd apps/backend
poetry install
```

2. Configure a API LLM no `.env`:

```bash
# Escolha uma das opções abaixo:

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

- `http://localhost:8000/` → página com formulário para texto e upload `.txt/.pdf`

## Uso da API

`POST /api/classify` (multipart/form-data)

Campos:
- `text` (opcional) — texto do email
- `file` (opcional) — arquivo `.txt` ou `.pdf`

Resposta (JSON):

```json
{
  "category": "Produtivo" | "Improdutivo",
  "reason": "string",
  "suggested_reply": "string"
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
2. Configure as variáveis de ambiente:
   - `LLM_PROVIDER=google`
   - `GOOGLE_API_KEY=sua_chave_aqui`
   - `GOOGLE_MODEL=gemini-2.0-flash`
3. Deploy automático será executado

### Outras opções
- Backend: Render / Fly.io
- Frontend: já é servido pelo backend. Alternativamente, hospedar `apps/frontend` em Vercel e apontar para a API pública.

## Variáveis suportadas

- `LLM_PROVIDER`: `openai`, `anthropic`, `google`, `ollama`
- `OPENAI_API_KEY`: chave da OpenAI (se `LLM_PROVIDER=openai`)
- `OPENAI_MODEL`: modelo da OpenAI (padrão `gpt-4o-mini`)
- `ANTHROPIC_API_KEY`: chave da Anthropic (se `LLM_PROVIDER=anthropic`)
- `ANTHROPIC_MODEL`: modelo da Anthropic (padrão `claude-3-haiku-20240307`)
- `GOOGLE_API_KEY`: chave do Google (se `LLM_PROVIDER=google`)
- `GOOGLE_MODEL`: modelo do Google (padrão `gemini-1.5-flash`)
- `OLLAMA_BASE_URL`: URL do Ollama (se `LLM_PROVIDER=ollama`)
- `OLLAMA_MODEL`: modelo do Ollama (padrão `llama3.2`)
