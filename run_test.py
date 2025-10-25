# run_test.py

from logos.client import Client

def main():
    print("--- Инициализация клиента Логос ---")
    logos_client = Client(llm_provider="openai", api_key="DUMMY_API_KEY")

    # --- ИЗМЕНЕНИЕ: Шаг 1 - Загружаем и именуем наш набор правил ---
    logos_client.load_ruleset(name="compliance", filepath="compliance_rules.json")

    print("\n--- Запуск теста: 'Движок Правил - Успешная проверка' ---")
    # ИЗМЕНЕНИЕ: Промпт теперь ссылается на имя 'compliance', а не на файл
    valid_prompt = "Проверь транзакцию с amount=9500 risk_score=0.7 transaction_hour=15 по набору правил 'compliance'"
    response = logos_client.run(valid_prompt)
    print("--- Ответ от клиента Логос ---")
    print(response)
    print("------------------------------")
    
    print("\n--- Запуск теста: 'Движок Правил - Неуспешная проверка' ---")
    invalid_prompt = "Проверь транзакцию с amount=12000 risk_score=0.5 transaction_hour=11 по набору правил 'compliance'"
    response = logos_client.run(invalid_prompt)
    print("--- Ответ от клиента Логос ---")
    print(response)
    print("------------------------------")

if __name__ == "__main__":
    main()
