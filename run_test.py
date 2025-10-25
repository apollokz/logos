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
    try:
        logos_client = Client(llm_provider="openai", api_key="DUMMY_API_KEY")
    except Exception as e:
        print(f"Ошибка при инициализации клиента: {e}")
        return

    # --- Тест 1: Задача на планирование (регрессионный тест) ---
    scheduling_prompt = "Мне нужно запланировать три встречи: A, B и C..."
    run_test_scenario(logos_client, "Планирование встреч", scheduling_prompt)

    # --- Тест 2: Новая задача на алгебру ---
    algebra_prompt = "Реши x + 2*y == 7, где x > 2 и y < 10."
    run_test_scenario(logos_client, "Решение уравнения", algebra_prompt)

    print("\n--- Все тесты завершены ---")

if __name__ == "__main__":
    main()
