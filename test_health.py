#!/usr/bin/env python3
"""
Script para testar o health check localmente
"""

import requests
import time
import sys

def test_health_check(url="http://localhost:8000"):
    """Testa o health check da aplicação"""
    print(f"🔍 Testando health check em {url}")
    
    try:
        # Testar endpoint root
        print("📡 Testando endpoint root...")
        response = requests.get(f"{url}/", timeout=10)
        print(f"✅ Root: {response.status_code} - {response.json()}")
        
        # Testar endpoint health
        print("📡 Testando endpoint health...")
        response = requests.get(f"{url}/health", timeout=10)
        print(f"✅ Health: {response.status_code} - {response.json()}")
        
        # Testar endpoint docs
        print("📡 Testando endpoint docs...")
        response = requests.get(f"{url}/docs", timeout=10)
        print(f"✅ Docs: {response.status_code}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - Aplicação não está rodando")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout - Aplicação demorou para responder")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def wait_for_app(url="http://localhost:8000", max_attempts=30):
    """Aguarda a aplicação ficar disponível"""
    print(f"⏳ Aguardando aplicação ficar disponível em {url}")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ Aplicação disponível após {attempt + 1} tentativas")
                return True
        except:
            pass
        
        print(f"⏳ Tentativa {attempt + 1}/{max_attempts}...")
        time.sleep(2)
    
    print("❌ Aplicação não ficou disponível no tempo esperado")
    return False

if __name__ == "__main__":
    print("🧪 Teste de Health Check")
    print("=" * 40)
    
    # Aguardar aplicação
    if not wait_for_app():
        print("❌ Falha no teste - Aplicação não disponível")
        sys.exit(1)
    
    # Testar health check
    if test_health_check():
        print("✅ Todos os testes passaram!")
    else:
        print("❌ Alguns testes falharam")
        sys.exit(1)
