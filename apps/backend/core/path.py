from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]   # apps/backend
APPS_DIR = BACKEND_DIR.parent                       # apps
FRONTEND_DIR = APPS_DIR / "frontend"
PROMPTS_DIR = BACKEND_DIR / "email_classifier_llm" / "prompts"