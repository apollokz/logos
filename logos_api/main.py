# logos_api/main.py

import os
from fastapi import FastAPI, Security, HTTPException
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles # ИЗМЕНЕНИЕ: Импортируем StaticFiles
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN

from logos.client import Client

# --- Конфигурация Безопасности ---

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
SECRET_API_KEY = "LOGOS_SECRET_MVP2_KEY"

async def get_api_key(api_key: str = Security(api_key_header)):
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

@app.post("/api/verify", response_model=VerificationResponse, tags=["Verification"]) # ИЗМЕНЕНИЕ: Добавили префикс /api
async def verify_prompt(request: VerificationRequest, api_key: str = Security(get_api_key)):
    """
    Основной эндпоинт для верификации (ЗАЩИЩЕННЫЙ).
    """
    verification_result = logos_client.run(request.prompt)
    return VerificationResponse(result=verification_result)

# --- Раздача Статики (Frontend) ---
# ВАЖНО: Этот вызов должен идти после определения всех API эндпоинтов.
app.mount("/", StaticFiles(directory="logos_api/static", html=True), name="static")
