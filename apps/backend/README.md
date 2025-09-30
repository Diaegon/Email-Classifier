# Email Classifier LLM - Backend

API para classificação de emails usando LLMs (OpenAI, Anthropic, Google Gemini, Ollama).

## Configuração

1. Copie o arquivo de exemplo de configuração:
   ```bash
   copy env.example .env
   ```

2. Configure as variáveis de ambiente no arquivo `.env` com sua chave de API preferida.

3. Instale as dependências:
   ```bash
   pip install -e .
   ```

## Execução

```bash
uvicorn email_classifier_llm.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /health` - Health check
- `POST /api/classify` - Classificar email
- `GET /` - Interface frontend

## Estrutura

- `main.py` - Aplicação FastAPI principal
- `routers/` - Endpoints da API
- `services/` - Lógica de negócio e integração com LLMs
