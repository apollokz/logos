# tests/test_logos_core.py

import pytest
from logos.client import Client

@pytest.fixture
def logos_client():
    """
    Эта 'фикстура' создает и предоставляет экземпляр клиента
    для каждого теста, который его запросит.
    """
    client = Client(llm_provider="openai", api_key="DUMMY_API_KEY")
    client.load_ruleset(name="compliance", filepath="compliance_rules.json")
    return client

def test_scheduling(logos_client):
    """Тестирует решатель задач планирования."""
    prompt = "Мне нужно запланировать три встречи: A, B и C..."
    response = logos_client.run(prompt)
    assert "Возможное расписание" in response
    assert "[Проверено Логос: Данное расписание удовлетворяет всем ограничениям.]" in response

def test_integer_algebra(logos_client):
    """Тестирует решатель целочисленной алгебры."""
    prompt = "Реши уравнение 3*x - y == 5, где x > 0 и y > 0."
    response = logos_client.run(prompt)
    assert "Решение найдено: x = 2, y = 1" in response

def test_real_algebra(logos_client):
    """Тестирует решатель алгебры с вещественными числами."""
    prompt = "Реши 2.5*a + b == 10.5, где a > 1 и b > 1."
    response = logos_client.run(prompt)
    assert "a = 3.4" in response  # Проверяем основной результат

def test_boolean_logic(logos_client):
    """Тестирует решатель булевой логики."""
    prompt = "Если Алиса идет на вечеринку, то Боб не идет. Если Клара не идет, то Алиса идет. Клара точно не пойдет."
    response = logos_client.run(prompt)
    assert "Алиса = True" in response
    assert "Боб = False" in response
    assert "Клара = False" in response

def test_rule_engine_valid(logos_client):
    """Тестирует Движок Правил на валидном сценарии."""
    prompt = "Проверь транзакцию с amount=9500 risk_score=0.7 transaction_hour=15 по набору правил 'compliance'"
    response = logos_client.run(prompt)
    assert "Проверка пройдена" in response

def test_rule_engine_invalid_and_audit(logos_client):
    """Тестирует Движок Правил на невалидном сценарии и проверяет детальный аудит."""
    prompt = "Проверь транзакцию с amount=12000 risk_score=0.5 transaction_hour=11 по набору правил 'compliance'"
    response = logos_client.run(prompt)
    assert "Проверка провалена" in response
    assert "Нарушено правило 'amount < 10000'" in response
    assert "(фактическое значение: amount = 12000)" in response
