from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any, Dict
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential
from core.path import PROMPTS_DIR
from core.config import get_settings

from google import genai

# Prompt centralizado para classificação de emails
class LLMClient(ABC):
    """Base class for LLM clients"""    
    @abstractmethod
    async def classify(self, text: str) -> Dict[str, Any]:
        """Classify text and return standardized result"""
        pass

class GoogleClient(LLMClient):
    """Google Gemini API client"""
    
    def __init__(self) -> None:        
        settings = get_settings()
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY).aio
        self.prompt_template = self._load_prompt()

    def _load_prompt(self) -> str:
        path = PROMPTS_DIR / "prompt_v1.txt"
        if not path.exists():
            raise RuntimeError(f"Prompt não encontrado: {path}")
        return path.read_text(encoding="utf-8")

    async def classify(self, text: str) -> Dict[str, Any]:
        prompt = self._build_prompt(text)
        content = await self._call_model(prompt)
        print('content', content)
        return self._parse_response(content)

    def _build_prompt(self, text: str) -> str:
        return self.prompt_template.format(text=text)


    #@retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
    async def _call_model(self, prompt: str) -> str:
        response = await self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt)
        return response.text

    def _parse_response(self, content: str) -> Dict[str, Any]:
        try:
            # Extract JSON from response
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = content[start:end]
                data = json.loads(json_str)
                return {
                    "category": data.get("category", "Improdutivo"),
                    "reason": data.get("reason", "Não foi possível analisar o conteúdo"),
                    "suggested_reply": data.get("suggested_reply", "Obrigado pelo contato!")
                }
        except (json.JSONDecodeError, ValueError):
            pass
        
        return {
            "category": "Improdutivo",
            "reason": "Falha ao interpretar resposta da IA",
            "suggested_reply": "Desculpe, não foi possível processar sua mensagem."
        }



# class OpenAIClient(LLMClient):
#     """OpenAI API client"""
    
#     def __init__(self) -> None:
#         from openai import AsyncOpenAI
        
#         settings = get_settings()
#         if not settings.openai_api_key:
#             raise ValueError("OPENAI_API_KEY not found in environment")
        
#         self._client = AsyncOpenAI(api_key=settings.openai_api_key)
#         self._model = settings.openai_model

#     @retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
#     async def classify(self, text: str) -> Dict[str, Any]:
#         prompt = self._build_prompt(text)
        
#         response = await self._client.chat.completions.create(
#             model=self._model,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.2,
#             response_format={"type": "json_object"},
#         )
        
#         content = response.choices[0].message.content or "{}"
#         return self._parse_response(content)

#     def _build_prompt(self, text: str) -> str:
#         return EMAIL_CLASSIFICATION_PROMPT.format(text=text)

#     def _parse_response(self, content: str) -> Dict[str, Any]:
#         try:
#             data = json.loads(content)
#             return {
#                 "category": data.get("category", "Improdutivo"),
#                 "reason": data.get("reason", "Não foi possível analisar o conteúdo"),
#                 "suggested_reply": data.get("suggested_reply", "Obrigado pelo contato!")
#             }
#         except json.JSONDecodeError:
#             return {
#                 "category": "Improdutivo",
#                 "reason": "Falha ao interpretar resposta da IA",
#                 "suggested_reply": "Desculpe, não foi possível processar sua mensagem."
#             }


# class AnthropicClient(LLMClient):
#     """Anthropic Claude API client"""
    
#     def __init__(self) -> None:
#         import anthropic
        
#         settings = get_settings()
#         if not settings.anthropic_api_key:
#             raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
#         self._client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
#         self._model = settings.anthropic_model

#     @retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
#     async def classify(self, text: str) -> Dict[str, Any]:
#         prompt = self._build_prompt(text)
        
#         response = await self._client.messages.create(
#             model=self._model,
#             max_tokens=1000,
#             temperature=0.2,
#             messages=[{"role": "user", "content": prompt}]
#         )
        
#         content = response.content[0].text
#         return self._parse_response(content)

#     def _build_prompt(self, text: str) -> str:
#         return EMAIL_CLASSIFICATION_PROMPT.format(text=text)

#     def _parse_response(self, content: str) -> Dict[str, Any]:
#         try:
#             # Extract JSON from response
#             start = content.find('{')
#             end = content.rfind('}') + 1
#             if start != -1 and end != 0:
#                 json_str = content[start:end]
#                 data = json.loads(json_str)
#                 return {
#                     "category": data.get("category", "Improdutivo"),
#                     "reason": data.get("reason", "Não foi possível analisar o conteúdo"),
#                     "suggested_reply": data.get("suggested_reply", "Obrigado pelo contato!")
#                 }
#         except (json.JSONDecodeError, ValueError):
#             pass
        
#         return {
#             "category": "Improdutivo",
#             "reason": "Falha ao interpretar resposta da IA",
#             "suggested_reply": "Desculpe, não foi possível processar sua mensagem."
#         }



# class OllamaClient(LLMClient):
#     """Ollama local API client"""
    
#     def __init__(self) -> None:
#         import httpx
        
#         settings = get_settings()
#         self._base_url = settings.ollama_base_url
#         self._model = settings.ollama_model
#         self._client = httpx.AsyncClient(timeout=60.0)

#     @retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
#     async def classify(self, text: str) -> Dict[str, Any]:
#         prompt = self._build_prompt(text)
        
#         response = await self._client.post(
#             f"{self._base_url}/api/generate",
#             json={
#                 "model": self._model,
#                 "prompt": prompt,
#                 "stream": False,
#                 "options": {"temperature": 0.2}
#             }
#         )
#         response.raise_for_status()
        
#         data = response.json()
#         content = data.get("response", "")
#         return self._parse_response(content)

#     def _build_prompt(self, text: str) -> str:
#         return EMAIL_CLASSIFICATION_PROMPT.format(text=text)

#     def _parse_response(self, content: str) -> Dict[str, Any]:
#         try:
#             # Extract JSON from response
#             start = content.find('{')
#             end = content.rfind('}') + 1
#             if start != -1 and end != 0:
#                 json_str = content[start:end]
#                 data = json.loads(json_str)
#                 return {
#                     "category": data.get("category", "Improdutivo"),
#                     "reason": data.get("reason", "Não foi possível analisar o conteúdo"),
#                     "suggested_reply": data.get("suggested_reply", "Obrigado pelo contato!")
#                 }
#         except (json.JSONDecodeError, ValueError):
#             pass
        
#         return {
#             "category": "Improdutivo",
#             "reason": "Falha ao interpretar resposta da IA",
#             "suggested_reply": "Desculpe, não foi possível processar sua mensagem."
#         }


def get_llm_client() -> LLMClient:
    return GoogleClient()
