from __future__ import annotations

import io
import re
from typing import Final

from pypdf import PdfReader

TXT_EXTENSIONS: Final = {".txt"}
PDF_EXTENSIONS: Final = {".pdf"}


def _ext_of(filename: str) -> str:
    lower = filename.lower()
    dot = lower.rfind(".")
    return lower[dot:] if dot != -1 else ""


def extract_text_from_file(*, filename: str, content: bytes) -> str:
    ext = _ext_of(filename)
    if ext in TXT_EXTENSIONS or ext == "":
        # Tenta decodificação robusta: BOMs e fallbacks comuns do Windows
        def _post(text: str) -> str:
            # Remove null chars e normaliza espaços
            return text.replace("\x00", "").strip()

        if content.startswith(b"\xef\xbb\xbf"):  # UTF-8 BOM
            try:
                return _post(content.decode("utf-8-sig"))
            except Exception:
                pass
        if content.startswith(b"\xff\xfe"):  # UTF-16 LE BOM
            try:
                return _post(content.decode("utf-16-le"))
            except Exception:
                pass
        if content.startswith(b"\xfe\xff"):  # UTF-16 BE BOM
            try:
                return _post(content.decode("utf-16-be"))
            except Exception:
                pass
        # Tentativas por ordem de probabilidade em Windows
        for encoding in ("utf-8", "utf-16", "cp1252", "latin-1"):
            try:
                return _post(content.decode(encoding))
            except Exception:
                continue
        # Último recurso: ignorar erros em utf-8
        return _post(content.decode("utf-8", errors="ignore"))
    
    if ext in PDF_EXTENSIONS:
        with io.BytesIO(content) as bio:
            reader = PdfReader(bio)
            pages_text = [page.extract_text() or "" for page in reader.pages]
            joined = "\n".join(pages_text)
            return joined.strip()
    
    raise ValueError("Unsupported file type. Use .txt or .pdf")


def preprocess_text(text: str) -> str:
    # Normaliza quebras de linha e reduz espaços
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Remove espaços à direita em cada linha e linhas vazias no fim/início
    lines = [ln.rstrip() for ln in text.split("\n")]
    # Rejunta e colapsa múltiplos espaços em um
    joined = "\n".join(lines).strip()
    joined = re.sub(r"\s+", " ", joined)
    return joined.strip()
