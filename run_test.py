# run_test.py

from logos.client import Client

def run_test_scenario(logos_client, test_name, prompt):
    """Функция для запуска одного тестового сценария."""
    print(f"\n--- Запуск теста: '{test_name}' ---")
    try:
        response = logos_client.run(prompt)
        print("--- Ответ от клиента Логос ---")
        print(response)
        print("------------------------------")
    except Exception as e:
        print(f"Ошибка при выполнении теста '{test_name}': {e}")

def main():
    """
    Основная функция для демонстрации работы клиента "Логос".
    """
    print("--- Инициализация клиента Логос MVP1 ---")
    logos_client = Client(llm_provider="openai", api_key="DUMMY_API_KEY")

    # --- Регрессионные тесты ---
    scheduling_prompt = "Мне нужно запланировать три встречи: A, B и C..."
    run_test_scenario(logos_client, "Планирование встреч", scheduling_prompt)
    
    integer_algebra_prompt = "Реши уравнение 3*x - y == 5, где x > 0 и y > 0."
    run_test_scenario(logos_client, "Целочисленная алгебра", integer_algebra_prompt)
    
    real_algebra_prompt = "Реши 2.5*a + b == 10.5, где a > 1 и b > 1."
    run_test_scenario(logos_client, "Алгебра с вещественными числами", real_algebra_prompt)

    # --- ИЗМЕНЕНИЕ: Тест 4: Новая задача на булеву логику ---
    boolean_prompt = "Если Алиса идет на вечеринку, то Боб не идет. Если Клара не идет, то Алиса идет. Клара точно не пойдет. Кто в итоге пойдет на вечеринку?"
    run_test_scenario(logos_client, "Булева логика (SAT)", boolean_prompt)

    print("\n--- Все тесты завершены ---")

if __name__ == "__main__":
    main()
