from google import genai
from core.config import get_settings
settings = get_settings()
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=settings.GEMINI_API_KEY)
entrada = input("digite a sua pergunta: ")
response = client.models.generate_content(
    model="gemini-3-flash-preview", contents=entrada
)
print(response.text)
