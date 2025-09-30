from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any, Dict

from tenacity import retry, stop_after_attempt, wait_exponential

from .settings import get_settings

# Prompt centralizado para classificação de emails
EMAIL_CLASSIFICATION_PROMPT = """
Você é um assistente de classificação de emails corporativos, de uma empresa do setor financeiro, a empresa é a empresa XX
financeira que oferece serviços de gestão de carteiras, analise de perfomance, análise de risco e serviços de consultoria.
os clientes podem ser de clientes pessoais ou de clientes empresariais. onde cada um deles possuem um banco de dados
individualizado para eles, que contem informações basicas, portfólio de ativos fincanceiro, perfil de investidor, etc.

Analise o email abaixo e retorne:
1. Classificação: "Produtivo" ou "Improdutivo"
2. Resposta sugerida (se Produtivo, ofereça ajuda específica; se Improdutivo, seja cordial e breve)

Critérios:
- Produtivo: requer ação, resposta, contém dúvidas, solicitações, problemas técnicos
- Improdutivo: mensagens sociais, felicitações, agradecimentos genéricos

Email:
{text}

Retorne APENAS no formato JSON:
{{
  "category": "Produtivo" ou "Improdutivo",
  "reason": "explicação breve",
  "suggested_reply": "resposta sugerida"
}}
"""


class LLMClient(ABC):
    """Base class for LLM clients"""
    
    @abstractmethod
    async def classify(self, text: str) -> Dict[str, Any]:
        """Classify text and return standardized result"""
        pass


class OpenAIClient(LLMClient):
    """OpenAI API client"""
    
    def __init__(self) -> None:
        from openai import AsyncOpenAI
        
        settings = get_settings()
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._model = settings.openai_model

    @retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
    async def classify(self, text: str) -> Dict[str, Any]:
        prompt = self._build_prompt(text)
        
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        
        content = response.choices[0].message.content or "{}"
        return self._parse_response(content)

    def _build_prompt(self, text: str) -> str:
        return EMAIL_CLASSIFICATION_PROMPT.format(text=text)

    def _parse_response(self, content: str) -> Dict[str, Any]:
        try:
            data = json.loads(content)
            return {
                "category": data.get("category", "Improdutivo"),
                "reason": data.get("reason", "Não foi possível analisar o conteúdo"),
                "suggested_reply": data.get("suggested_reply", "Obrigado pelo contato!")
            }
        except json.JSONDecodeError:
            return {
                "category": "Improdutivo",
                "reason": "Falha ao interpretar resposta da IA",
                "suggested_reply": "Desculpe, não foi possível processar sua mensagem."
            }


class AnthropicClient(LLMClient):
    """Anthropic Claude API client"""
    
    def __init__(self) -> None:
        import anthropic
        
        settings = get_settings()
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
        self._client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        self._model = settings.anthropic_model

    @retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
    async def classify(self, text: str) -> Dict[str, Any]:
        prompt = self._build_prompt(text)
        
        response = await self._client.messages.create(
            model=self._model,
            max_tokens=1000,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        return self._parse_response(content)

    def _build_prompt(self, text: str) -> str:
        return EMAIL_CLASSIFICATION_PROMPT.format(text=text)

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


class GoogleClient(LLMClient):
    """Google Gemini API client"""
    
    def __init__(self) -> None:
        import google.generativeai as genai
        
        settings = get_settings()
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")
        
        genai.configure(api_key=settings.google_api_key)
        self._model = genai.GenerativeModel(settings.google_model)

    @retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
    async def classify(self, text: str) -> Dict[str, Any]:
        prompt = self._build_prompt(text)
        
        # Google Generative AI não tem método async nativo, usar run_in_executor
        import asyncio
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self._model.generate_content, prompt)
        
        content = response.text
        
        return self._parse_response(content)

    def _build_prompt(self, text: str) -> str:
        return EMAIL_CLASSIFICATION_PROMPT.format(text=text)

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


class OllamaClient(LLMClient):
    """Ollama local API client"""
    
    def __init__(self) -> None:
        import httpx
        
        settings = get_settings()
        self._base_url = settings.ollama_base_url
        self._model = settings.ollama_model
        self._client = httpx.AsyncClient(timeout=60.0)

    @retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
    async def classify(self, text: str) -> Dict[str, Any]:
        prompt = self._build_prompt(text)
        
        response = await self._client.post(
            f"{self._base_url}/api/generate",
            json={
                "model": self._model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2}
            }
        )
        response.raise_for_status()
        
        data = response.json()
        content = data.get("response", "")
        return self._parse_response(content)

    def _build_prompt(self, text: str) -> str:
        return EMAIL_CLASSIFICATION_PROMPT.format(text=text)

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


def get_llm_client() -> LLMClient:
    """Factory function to get the appropriate LLM client based on configuration"""
    settings = get_settings()
    provider = settings.llm_provider
    
    if not provider:
        raise ValueError("LLM_PROVIDER not configured. Set to: openai, anthropic, google, or ollama")
    
    if provider == "openai":
        return OpenAIClient()
    elif provider == "anthropic":
        return AnthropicClient()
    elif provider == "google":
        return GoogleClient()
    elif provider == "ollama":
        return OllamaClient()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
