# logos_api/main.py
import os
from datetime import datetime
from fastapi import FastAPI, Security, HTTPException
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN
from typing import List
import stripe

from logos.client import Client

# --- Конфигурация Безопасности и Stripe ---
stripe.api_key = "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" 

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

# ИЗМЕНЕНИЕ 1: Модель ответа теперь отражает новую структуру из client.py
class VerificationResponse(BaseModel):
    result: str
    details: str
    triggered_rules: List[str]

class HistoryEntry(BaseModel):
    timestamp: str
    request_prompt: str
    response_result: str # Оставляем строкой для простоты лога

class CheckoutSessionResponse(BaseModel):
    session_id: str

# --- Инициализация и Хранилище ---
app = FastAPI(
    title="Logos API",
    description="API для верификации данных с помощью символического решателя.",
    version="0.2.0", # Версия Прометей
)

logos_client = Client(llm_provider="offline", api_key="DUMMY")
logos_client.load_ruleset("rulesets")
verification_history: List[HistoryEntry] = []

# --- API Эндпоинты ---

@app.post("/api/verify", response_model=VerificationResponse, tags=["Verification"])
async def verify_prompt(request: VerificationRequest, api_key: str = Security(get_api_key)):
    # ИЗМЕНЕНИЕ 2: Обрабатываем словарь, а не строку
    verification_result_dict = logos_client.run(request.prompt)
    
    # Для истории сохраняем краткую сводку, чтобы не менять модель HistoryEntry
    history_summary = f"Result: {verification_result_dict['result']}, Rules: {verification_result_dict['triggered_rules']}"
    
    entry = HistoryEntry(
        timestamp=datetime.utcnow().isoformat(),
        request_prompt=request.prompt,
        response_result=history_summary
    )
    verification_history.append(entry)
    
    # ИЗМЕНЕНИЕ 3: Возвращаем новый объект VerificationResponse, распаковывая словарь
    return VerificationResponse(**verification_result_dict)

@app.get("/api/history", response_model=List[HistoryEntry], tags=["History"])
async def get_history(api_key: str = Security(get_api_key)):
    return verification_history

@app.post("/api/create-checkout-session", response_model=CheckoutSessionResponse, tags=["Payments"])
async def create_checkout_session(api_key: str = Security(get_api_key)):
    try:
        YOUR_DOMAIN = "http://62.169.19.122:8000" 
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Logos Platform - Pro Subscription',
                        },
                        'unit_amount': 2000,
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
