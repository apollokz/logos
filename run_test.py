# run_test.py

from logos.client import Client

def run_test_scenario(logos_client, test_name, prompt):
    print(f"\n--- Запуск теста: '{test_name}' ---")
    try:
        response = logos_client.run(prompt)
        print("--- Ответ от клиента Логос ---")
        print(response)
        print("------------------------------")
    except Exception as e:
        print(f"Ошибка при выполнении теста '{test_name}': {e}")

def main():
    print("--- Инициализация клиента Логос ---")
    logos_client = Client(llm_provider="openai", api_key="DUMMY_API_KEY")

    # --- MVP1 Тесты (регрессия) ---
    # ... (предыдущие тесты)

    # --- ИЗМЕНЕНИЕ: MVP2 Тест: Движок Правил ---
    # Сценарий 1: Валидная транзакция
    rule_engine_valid_prompt = "Проверь транзакцию с amount=9500 risk_score=0.7 transaction_hour=15 по набору правил 'compliance_rules.json'"
    run_test_scenario(logos_client, "Движок Правил - Успешная проверка", rule_engine_valid_prompt)
    
    # Сценарий 2: Невалидная транзакция (сумма слишком большая)
    rule_engine_invalid_prompt = "Проверь транзакцию с amount=12000 risk_score=0.5 transaction_hour=11 по набору правил 'compliance_rules.json'"
    run_test_scenario(logos_client, "Движок Правил - Неуспешная проверка", rule_engine_invalid_prompt)


if __name__ == "__main__":
    main()
