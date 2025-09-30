# 🚀 Deploy no Railway com PostgreSQL

## 📋 Passo a Passo

### 1. **Configurar Projeto no Railway**

1. Acesse [Railway](https://railway.app)
2. Clique em "New Project"
3. Selecione "Deploy from GitHub repo"
4. Escolha seu repositório

### 2. **Adicionar Banco PostgreSQL**

1. No dashboard do Railway, clique em "New Service"
2. Selecione "Database" → "PostgreSQL"
3. Anote as credenciais geradas

### 3. **Configurar Variáveis de Ambiente**

No dashboard do Railway, vá em "Variables" e adicione:

```env
# Banco de Dados (Railway gera automaticamente)
DB_DATABASE_URL=${{Postgres.DATABASE_URL}}

# LLM Provider (escolha uma)
LLM_PROVIDER=google
GOOGLE_API_KEY=sua_chave_aqui
GOOGLE_MODEL=gemini-2.0-flash

# Ou OpenAI
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sua_chave_aqui
# OPENAI_MODEL=gpt-4o-mini
```

### 4. **Deploy Automático**

O Railway irá:
- ✅ Instalar dependências automaticamente
- ✅ Executar migrações do banco
- ✅ Criar tabelas necessárias
- ✅ Iniciar a aplicação

### 5. **Verificar Deploy**

1. Acesse a URL fornecida pelo Railway
2. Teste a funcionalidade de busca de clientes
3. Verifique os logs em "Deployments" → "View Logs"

## 🔧 **Troubleshooting**

### **Erro de Conexão com Banco**
```bash
# Verificar se DB_DATABASE_URL está configurada
echo $DB_DATABASE_URL
```

### **Erro de Migrações**
```bash
# Executar migrações manualmente
cd apps/backend
python migrate.py init
python migrate.py upgrade
```

### **Logs de Deploy**
- Acesse "Deployments" no Railway
- Clique em "View Logs"
- Procure por mensagens de erro

## 📊 **Estrutura das Tabelas**

O sistema criará automaticamente:

```sql
-- Tabela de clientes
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255),
    cpf VARCHAR(14) UNIQUE,
    data_nascimento DATE,
    numero_cliente VARCHAR(50) UNIQUE,
    email VARCHAR(255) UNIQUE,
    perfil_investidor VARCHAR(50),
    ativos_custodiados TEXT,
    plano_contratual_em_dia BOOLEAN DEFAULT TRUE
);
```

## ✅ **Verificação de Sucesso**

1. **Health Check**: `https://seu-app.railway.app/health`
2. **API Docs**: `https://seu-app.railway.app/docs`
3. **Frontend**: `https://seu-app.railway.app/`
4. **Busca de Clientes**: Teste a funcionalidade de busca

## 🚨 **Importante**

- **SQLite não funciona** em produção no Railway
- **Use PostgreSQL** para persistência de dados
- **Configure as variáveis** de ambiente corretamente
- **Monitore os logs** durante o deploy

## 📞 **Suporte**

Se encontrar problemas:
1. Verifique os logs do Railway
2. Confirme as variáveis de ambiente
3. Teste a conexão com o banco
4. Verifique se as migrações executaram
