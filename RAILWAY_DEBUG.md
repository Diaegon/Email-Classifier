# 🐛 Debug de Health Check no Railway

## 🔍 **Problemas Comuns e Soluções**

### **1. Health Check Timeout**
**Sintoma**: `Health check failed: timeout`
**Causa**: Aplicação demora para iniciar
**Solução**: 
- ✅ Aumentar `healthcheckTimeout` para 600s
- ✅ Verificar se migrações estão demorando
- ✅ Adicionar logs detalhados

### **2. Porta Incorreta**
**Sintoma**: `Connection refused`
**Causa**: Aplicação não está na porta correta
**Solução**:
- ✅ Usar `os.getenv("PORT", 8000)`
- ✅ Verificar logs de inicialização
- ✅ Testar localmente primeiro

### **3. Banco de Dados Não Conecta**
**Sintoma**: `Database connection failed`
**Causa**: PostgreSQL não está acessível
**Solução**:
- ✅ Verificar `DB_DATABASE_URL`
- ✅ Aguardar PostgreSQL inicializar
- ✅ Testar conexão manualmente

## 🛠️ **Como Debuggar**

### **1. Verificar Logs do Railway**
```bash
# No dashboard do Railway:
# 1. Vá em "Deployments"
# 2. Clique no deploy mais recente
# 3. Clique em "View Logs"
# 4. Procure por erros
```

### **2. Testar Health Check Manualmente**
```bash
# Após o deploy, teste:
curl https://seu-app.railway.app/health
curl https://seu-app.railway.app/
```

### **3. Verificar Variáveis de Ambiente**
```bash
# No Railway, vá em "Variables" e confirme:
DB_DATABASE_URL=${{Postgres.DATABASE_URL}}
LLM_PROVIDER=google
GOOGLE_API_KEY=sua_chave
```

## 🔧 **Configurações Atualizadas**

### **railway.json**
```json
{
  "deploy": {
    "healthcheckPath": "/health",
    "healthcheckTimeout": 600,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 5
  }
}
```

### **Health Check Endpoint**
```python
@app.get("/health")
def health():
    try:
        # Testa conexão com banco
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

## 📊 **Logs Esperados**

### **Deploy Bem-sucedido:**
```
🔄 Inicializando banco de dados...
✅ Banco de dados inicializado com sucesso!
🚀 Iniciando aplicação...
📡 Porta configurada: 8000
✅ Uvicorn importado com sucesso
✅ Configuração do Uvicorn criada
✅ Servidor Uvicorn criado
🌐 Iniciando servidor na porta 8000...
INFO: Started server process
INFO: Waiting for application startup
INFO: Application startup complete
```

### **Health Check Bem-sucedido:**
```json
{
  "status": "healthy",
  "message": "Email Classifier API is running",
  "database": "connected",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 🚨 **Troubleshooting Rápido**

### **Se o deploy falhar:**
1. Verifique os logs do Railway
2. Confirme as variáveis de ambiente
3. Teste localmente primeiro
4. Verifique se o PostgreSQL está rodando

### **Se o health check falhar:**
1. Acesse `/health` manualmente
2. Verifique se o banco está conectado
3. Confirme se a aplicação está rodando
4. Verifique os logs de erro

### **Se a aplicação não iniciar:**
1. Verifique se todas as dependências estão instaladas
2. Confirme se o Python está na versão correta
3. Verifique se não há erros de sintaxe
4. Teste o script `deploy.py` localmente

## ✅ **Checklist de Deploy**

- [ ] Variáveis de ambiente configuradas
- [ ] PostgreSQL adicionado e funcionando
- [ ] Logs mostram inicialização bem-sucedida
- [ ] Health check responde com status 200
- [ ] Frontend carrega corretamente
- [ ] API de clientes funciona
- [ ] API de classificação funciona
