from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # apps/

FRONTEND_DIR = BASE_DIR / "frontend"
BACKEND_DIR = BASE_DIR / "backend"

PROMTPTS_DIR = BACKEND_DIR / "email_classifier_llm" / "prompts"