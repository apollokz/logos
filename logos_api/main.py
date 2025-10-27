# logos_api/main.py

import os
from datetime import datetime
from fastapi import FastAPI, Security, HTTPException
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN
from typing import List # ИЗМЕНЕНИЕ: Добавляем List для типизации

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

# ИЗМЕНЕНИЕ: Новая модель для хранения записи в истории
class HistoryEntry(BaseModel):
    timestamp: str
    request_prompt: str
    response_result: str

# --- Инициализация и Хранилище ---

app = FastAPI(
    title="Logos API",
    description="API для верификации данных с помощью символического решателя.",
    version="0.1.0",
)

logos_client = Client(llm_provider="offline", api_key="DUMMY")
logos_client.load_ruleset("rulesets")

# ИЗМЕНЕНИЕ: Создаем простое хранилище в памяти
verification_history: List[HistoryEntry] = []

# --- API Эндпоинты ---

@app.post("/api/verify", response_model=VerificationResponse, tags=["Verification"])
async def verify_prompt(request: VerificationRequest, api_key: str = Security(get_api_key)):
    """
    Основной эндпоинт для верификации (ЗАЩИЩЕННЫЙ).
    """
    verification_result = logos_client.run(request.prompt)
    
    # ИЗМЕНЕНИЕ: Сохраняем запись о запросе в историю
    entry = HistoryEntry(
        timestamp=datetime.utcnow().isoformat(),
        request_prompt=request.prompt,
        response_result=verification_result
    )
    verification_history.append(entry)
    
    return VerificationResponse(result=verification_result)

# ИЗМЕНЕНИЕ: Новый эндпоинт для получения истории
@app.get("/api/history", response_model=List[HistoryEntry], tags=["History"])
async def get_history(api_key: str = Security(get_api_key)):
    """
    Возвращает историю запросов на верификацию (ЗАЩИЩЕННЫЙ).
    """
    return verification_history

# --- Раздача Статики (Frontend) ---
app.mount("/", StaticFiles(directory="logos_api/static", html=True), name="static")
