# logos_api/main.py

import os
from fastapi import FastAPI, Security, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN

from logos.client import Client

# --- Конфигурация Безопасности ---

# Определяем, что API ключ будет передаваться в заголовке X-API-Key
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Наш секретный ключ. В реальном приложении он будет загружаться из переменных окружения.
# Для простоты MVP2 мы его временно захардкодим.
SECRET_API_KEY = "LOGOS_SECRET_MVP2_KEY"

async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Зависимость, которая проверяет предоставленный API ключ.
    """
    if api_key == SECRET_API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

# --- Модели данных (API Контракт) ---

class VerificationRequest(BaseModel):
    prompt: str

class VerificationResponse(BaseModel):
    result: str

# --- Инициализация приложения и движка "Логос" ---

app = FastAPI(
    title="Logos API",
    description="API для верификации данных с помощью символического решателя.",
    version="0.1.0",
)

logos_client = Client(llm_provider="offline", api_key="DUMMY")
logos_client.load_ruleset("rulesets")

# --- API Эндпоинты ---

@app.get("/", tags=["Status"])
async def read_root():
    return {"status": "ok", "message": "Logos API is running successfully."}

@app.post("/verify", response_model=VerificationResponse, tags=["Verification"])
async def verify_prompt(request: VerificationRequest, api_key: str = Security(get_api_key)):
    """
    Основной эндпоинт для верификации (ЗАЩИЩЕННЫЙ).
    Принимает промпт и возвращает результат от движка "Логос".
    Требует наличия валидного заголовка X-API-Key.
    """
    verification_result = logos_client.run(request.prompt)
    return VerificationResponse(result=verification_result)
