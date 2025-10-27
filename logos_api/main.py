# logos_api/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from logos.client import Client # Импортируем наш клиент

# --- Модели данных (API Контракт) ---
# Используем Pydantic для валидации входящих и исходящих данных

class VerificationRequest(BaseModel):
    """Модель для входящего запроса на верификацию."""
    prompt: str

class VerificationResponse(BaseModel):
    """Модель для ответа после верификации."""
    result: str

# --- Инициализация приложения и движка "Логос" ---

# Создаем экземпляр приложения FastAPI
app = FastAPI(
    title="Logos API",
    description="API для верификации данных с помощью символического решателя.",
    version="0.1.0",
)

# Создаем единый экземпляр клиента "Логос" при старте приложения
# Это эффективно, так как нам не нужно пересоздавать его при каждом запросе
logos_client = Client(llm_provider="offline", api_key="DUMMY")
logos_client.load_ruleset("rulesets") # Загружаем все правила из директории

# --- API Эндпоинты ---

@app.get("/", tags=["Status"])
async def read_root():
    """
    Корневой эндпоинт для проверки работоспособности API.
    """
    return {"status": "ok", "message": "Logos API is running successfully."}


@app.post("/verify", response_model=VerificationResponse, tags=["Verification"])
async def verify_prompt(request: VerificationRequest):
    """
    Основной эндпоинт для верификации.
    Принимает промпт и возвращает результат от движка "Логос".
    """
    # Выполняем верификацию с помощью нашего движка
    verification_result = logos_client.run(request.prompt)
    
    # Возвращаем результат в формате, соответствующем нашей response_model
    return VerificationResponse(result=verification_result)
