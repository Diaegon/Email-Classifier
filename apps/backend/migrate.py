#!/usr/bin/env python3
"""
Script de gerenciamento de migrações do banco de dados
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd):
    """Executa um comando e retorna o resultado"""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando: {e}")
        print(f"Stderr: {e.stderr}")
        return False


def init_migrations():
    """Inicializa o sistema de migrações"""
    print("Inicializando sistema de migrações...")
    return run_command("alembic init migrations")


def create_migration(message):
    """Cria uma nova migração"""
    print(f"Criando migração: {message}")
    return run_command(f'alembic revision --autogenerate -m "{message}"')


def upgrade_database(revision="head"):
    """Aplica migrações ao banco de dados"""
    print(f"Aplicando migrações até: {revision}")
    return run_command(f"alembic upgrade {revision}")


def downgrade_database(revision):
    """Reverte migrações do banco de dados"""
    print(f"Revertendo migrações para: {revision}")
    return run_command(f"alembic downgrade {revision}")


def show_history():
    """Mostra o histórico de migrações"""
    print("Histórico de migrações:")
    return run_command("alembic history")


def show_current():
    """Mostra a migração atual"""
    print("Migração atual:")
    return run_command("alembic current")


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("""
Uso: python migrate.py <comando> [argumentos]

Comandos disponíveis:
  init                    - Inicializa o sistema de migrações
  create <mensagem>       - Cria uma nova migração
  upgrade [revisão]       - Aplica migrações (padrão: head)
  downgrade <revisão>     - Reverte migrações
  history                 - Mostra histórico de migrações
  current                 - Mostra migração atual
  help                    - Mostra esta ajuda
        """)
        return

    command = sys.argv[1].lower()

    if command == "init":
        init_migrations()
    elif command == "create":
        if len(sys.argv) < 3:
            print("Erro: Forneça uma mensagem para a migração")
            print("Exemplo: python migrate.py create 'Adicionar tabela de usuários'")
            return
        message = " ".join(sys.argv[2:])
        create_migration(message)
    elif command == "upgrade":
        revision = sys.argv[2] if len(sys.argv) > 2 else "head"
        upgrade_database(revision)
    elif command == "downgrade":
        if len(sys.argv) < 3:
            print("Erro: Forneça uma revisão para reverter")
            print("Exemplo: python migrate.py downgrade -1")
            return
        revision = sys.argv[2]
        downgrade_database(revision)
    elif command == "history":
        show_history()
    elif command == "current":
        show_current()
    elif command == "help":
        print("""
Uso: python migrate.py <comando> [argumentos]

Comandos disponíveis:
  init                    - Inicializa o sistema de migrações
  create <mensagem>       - Cria uma nova migração
  upgrade [revisão]       - Aplica migrações (padrão: head)
  downgrade <revisão>     - Reverte migrações
  history                 - Mostra histórico de migrações
  current                 - Mostra migração atual
  help                    - Mostra esta ajuda
        """)
    else:
        print(f"Comando desconhecido: {command}")
        print("Use 'python migrate.py help' para ver os comandos disponíveis")


if __name__ == "__main__":
    main()
