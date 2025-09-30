#!/usr/bin/env python3

import os
from email_classifier_llm.services.settings import get_settings

print(f"Current working directory: {os.getcwd()}")
print(f".env exists in current dir: {os.path.exists('.env')}")
print(f".env exists in apps/backend: {os.path.exists('apps/backend/.env')}")

# Limpar cache
get_settings.cache_clear()

# Testar configurações
try:
    settings = get_settings()
    print(f"\nSettings loaded successfully:")
    print(f"Provider: {settings.llm_provider}")
    print(f"Google Key: {settings.google_api_key[:10] if settings.google_api_key else 'None'}...")
    print(f"Google Model: {settings.google_model}")
except Exception as e:
    print(f"Error loading settings: {e}")
    import traceback
    traceback.print_exc()
