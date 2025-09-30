# Sistema de Migrações com Alembic

Este projeto usa o Alembic para gerenciar migrações do banco de dados, permitindo evolução do schema de forma controlada e versionada.

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na pasta `apps/backend/` com as seguintes configurações:

```env
# Para SQLite (desenvolvimento)
DB_DATABASE_URL=sqlite:///./email_classifier.db

# Para PostgreSQL (produção)
# DB_DATABASE_URL=postgresql://usuario:senha@localhost:5432/email_classifier

# Para MySQL (produção)
# DB_DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/email_classifier
```

### Instalação

```bash
cd apps/backend
pip install -e .
```

## Comandos Disponíveis

### Usando o script de migração (recomendado)

```bash
# Inicializar migrações (apenas na primeira vez)
python migrate.py init

# Criar nova migração
python migrate.py create "Adicionar tabela de usuários"

# Aplicar migrações
python migrate.py upgrade

# Reverter migração
python migrate.py downgrade -1

# Ver histórico
python migrate.py history

# Ver migração atual
python migrate.py current
```

### Usando Alembic diretamente

```bash
# Criar migração
alembic revision --autogenerate -m "Descrição da mudança"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1

# Ver histórico
alembic history

# Ver migração atual
alembic current
```

## Fluxo de Trabalho

### 1. Desenvolvimento Local

1. **Modifique os modelos** em `email_classifier_llm/models/`
2. **Crie uma migração**:
   ```bash
   python migrate.py create "Descrição da mudança"
   ```
3. **Revise o arquivo de migração** gerado em `migrations/versions/`
4. **Aplique a migração**:
   ```bash
   python migrate.py upgrade
   ```

### 2. Deploy em Produção

1. **Aplique as migrações**:
   ```bash
   python migrate.py upgrade
   ```

### 3. Rollback (se necessário)

1. **Reverta para migração anterior**:
   ```bash
   python migrate.py downgrade -1
   ```

## Estrutura de Arquivos

```
apps/backend/
├── alembic.ini                 # Configuração do Alembic
├── migrate.py                  # Script de gerenciamento
├── migrations/
│   ├── env.py                 # Configuração do ambiente
│   ├── script.py.mako         # Template para migrações
│   └── versions/              # Arquivos de migração
│       └── 0001_initial.py    # Migração inicial
└── email_classifier_llm/
    ├── database.py            # Configuração do banco
    └── models/                # Modelos SQLAlchemy
```

## Suporte a Diferentes Bancos

### SQLite (Desenvolvimento)
```env
DB_DATABASE_URL=sqlite:///./email_classifier.db
```

### PostgreSQL (Produção)
```env
DB_DATABASE_URL=postgresql://usuario:senha@localhost:5432/email_classifier
```

### MySQL (Produção)
```env
DB_DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/email_classifier
```

## Dicas Importantes

1. **Sempre revise** os arquivos de migração antes de aplicar
2. **Teste as migrações** em ambiente de desenvolvimento primeiro
3. **Faça backup** do banco antes de aplicar migrações em produção
4. **Use mensagens descritivas** ao criar migrações
5. **Mantenha as migrações pequenas** e focadas em uma mudança específica

## Troubleshooting

### Erro de conexão
- Verifique se a URL do banco está correta
- Confirme se o banco está rodando
- Verifique as credenciais

### Conflitos de migração
- Use `alembic merge` para resolver conflitos
- Revise o histórico com `alembic history`

### Migração falhou
- Revise os logs de erro
- Use `alembic downgrade` para reverter
- Corrija o problema e crie nova migração
