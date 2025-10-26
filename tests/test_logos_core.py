# tests/test_logos_core.py


import pytest
from logos.client import Client


@pytest.fixture
def logos_client():
    client = Client(llm_provider="openai", api_key="DUMMY_API_KEY")
    client.load_ruleset(name="compliance", filepath="compliance_rules.json")
    return client


def test_scheduling(logos_client):
    prompt = "Мне нужно запланировать три встречи: A, B и C..."
    response = logos_client.run(prompt)
    assert "Возможное расписание" in response


def test_integer_algebra(logos_client):
    prompt = "Реши уравнение 3*x - y == 5, где x > 0 и y > 0."
    response = logos_client.run(prompt)
    assert "x = 2, y = 1" in response


def test_real_algebra(logos_client):
    prompt = "Реши 2.5*a + b == 10.5, где a > 1 и b > 1."
    response = logos_client.run(prompt)
    assert ("a = 2, b = 5.5" in response) or ("a = 3.4" in response)


def test_boolean_logic(logos_client):
    prompt = "Если Алиса идет на вечеринку, то Боб не идет. Если Клара не идет, то Алиса идет. Клара точно не пойдет."
    response = logos_client.run(prompt)
    assert "Алиса = True" in response
    assert "Боб = False" in response
    assert "Клара = False" in response


def test_boolean_logic_dynamic(logos_client):
    prompt = "Если Иван работает, то Мария отдыхает. Если Петр не отдыхает, то Иван работает. Петр точно не отдыхает."
    response = logos_client.run(prompt)
    assert "Иван = True" in response
    assert "Мария = True" in response
    assert "Петр = False" in response


def test_rule_engine_valid_natural_language(logos_client):
    prompt = "Проверь транзакцию на сумму 9500 с оценкой риска 0.7 и в час 15 по набору правил 'compliance'"
    response = logos_client.run(prompt)
    assert "Проверка пройдена" in response


def test_rule_engine_invalid_natural_language(logos_client):
    prompt = "Проверь транзакцию на сумму 12000 с оценкой риска 0.5 и в час 11 по набору правил 'compliance'"
    response = logos_client.run(prompt)
    assert "Проверка провалена" in response
    assert "Нарушено правило 'amount < 10000'" in response
    assert "(фактическое значение: amount = 12000)" in response

# --- НОВЫЙ ТЕСТ ДЛЯ L2 ---
@pytest.mark.parametrize("prompt_format", [
    "Проверь транзакцию с amount=9500, risk_score: 0.7 и час 15 по набору правил 'compliance'",
    "Проверь транзакцию где сумма 9500, риск=0.7, transaction_hour: 15 по набору правил 'compliance'",
    "Проверь транзакцию: amount:9500 risk_score=0.7 час=15 по набору правил 'compliance'"
])
def test_rule_engine_flexible_formats(logos_client, prompt_format):
    """
    Проверяет, что NLP-парсер движка правил устойчив к разным форматам промпта.
    Все эти варианты должны быть валидными.
    """
    response = logos_client.run(prompt_format)
    assert "Проверка пройдена" in response
