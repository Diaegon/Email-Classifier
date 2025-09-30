from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional

from ..services.processor import extract_text_from_file, preprocess_text
from ..services.llm_client import get_llm_client

router = APIRouter(tags=["classify"])


@router.post("/classify")
async def classify(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    if not text and not file:
        raise HTTPException(status_code=400, detail="Provide 'text' or 'file'.")

    if file is not None:
        try:
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="Arquivo recebido está vazio (0 bytes).")
            text = extract_text_from_file(filename=file.filename, content=content)
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=400, detail=f"Failed to read file: {exc}")

    assert text is not None
    cleaned = preprocess_text(text)
    
    if not cleaned:
        # Fallback amigável: retorna 200 com mensagem explicativa
        return JSONResponse(
            {
                "category": "Improdutivo",
                "reason": "Arquivo sem conteúdo válido após extração (encoding/arquivo em branco).",
                "suggested_reply": "O arquivo enviado não pôde ser lido. Pode colar o texto diretamente ou reenviar o arquivo em .txt/.pdf?",
            }
        )

    try:
        # Get LLM client and classify
        llm_client = get_llm_client()
        result = await llm_client.classify(cleaned)
        return JSONResponse(result)
    except Exception as exc:
        return JSONResponse(
            {
                "category": "Improdutivo",
                "reason": f"Erro na classificação: {str(exc)}",
                "suggested_reply": "Desculpe, ocorreu um erro interno. Tente novamente em alguns instantes.",
            },
            status_code=500
        )
