# logos_api/main.py

import os
from datetime import datetime
from fastapi import FastAPI, Security, HTTPException
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN
from typing import List

# ИЗМЕНЕНИЕ: Импортируем stripe
import stripe

from logos.client import Client

# --- Конфигурация Безопасности и Stripe ---

# ВАЖНО: Используем тестовый ключ Stripe. Никогда не храните реальные ключи в коде.
# В реальном приложении этот ключ будет загружаться из переменных окружения.
stripe.api_key = "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" # ЗАМЕНИТЕ ЭТО ПОЗЖЕ НА СВОЙ ТЕСТОВЫЙ КЛЮЧ

# Наш внутренний API ключ
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

class HistoryEntry(BaseModel):
    timestamp: str
    request_prompt: str
    response_result: str

# ИЗМЕНЕНИЕ: Новая модель для ответа от эндпоинта Stripe
class CheckoutSessionResponse(BaseModel):
    session_id: str

# --- Инициализация и Хранилище ---

app = FastAPI(
    title="Logos API",
    description="API для верификации данных с помощью символического решателя.",
    version="0.1.0",
)

logos_client = Client(llm_provider="offline", api_key="DUMMY")
logos_client.load_ruleset("rulesets")

verification_history: List[HistoryEntry] = []

# --- API Эндпоинты ---

@app.post("/api/verify", response_model=VerificationResponse, tags=["Verification"])
async def verify_prompt(request: VerificationRequest, api_key: str = Security(get_api_key)):
    verification_result = logos_client.run(request.prompt)
    entry = HistoryEntry(
        timestamp=datetime.utcnow().isoformat(),
        request_prompt=request.prompt,
        response_result=verification_result
    )
    verification_history.append(entry)
    return VerificationResponse(result=verification_result)

@app.get("/api/history", response_model=List[HistoryEntry], tags=["History"])
async def get_history(api_key: str = Security(get_api_key)):
    return verification_history

# ИЗМЕНЕНИЕ: Новый эндпоинт для создания платежной сессии
@app.post("/api/create-checkout-session", response_model=CheckoutSessionResponse, tags=["Payments"])
async def create_checkout_session(api_key: str = Security(get_api_key)):
    """
    Создает платежную сессию Stripe Checkout и возвращает ее ID.
    """
    try:
        # URL, на которые Stripe перенаправит пользователя после оплаты
        # В нашем случае это просто главная страница
        YOUR_DOMAIN = "http://62.169.19.122:8000" # Используем ваш публичный IP

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Logos Platform - Pro Subscription',
                        },
                        'unit_amount': 2000, # $20.00 в центах
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '?status=success',
            cancel_url=YOUR_DOMAIN + '?status=canceled',
        )
        return CheckoutSessionResponse(session_id=checkout_session.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Раздача Статики (Frontend) ---
app.mount("/", StaticFiles(directory="logos_api/static", html=True), name="static")
