# run_test.py

# Импортируем наш класс Client из созданного пакета logos
from logos.client import Client

def main():
    """
    Основная функция для демонстрации работы клиента "Лogoс".
    """
    print("--- Запуск тестового сценария для Логос MVP1 ---")

    # Инициализируем клиент. На данном этапе api_key и provider - это заглушки.
    try:
        logos_client = Client(llm_provider="openai", api_key="DUMMY_API_KEY")
    except Exception as e:
        print(f"Ошибка при инициализации клиента: {e}")
        return

    # Определяем тестовый промпт, как в плейбуке
    test_prompt = "Мне нужно запланировать три встречи: A, B и C..."

    # Вызываем основной метод run
    try:
        response = logos_client.run(test_prompt)
        print("\n--- Ответ от клиента Логос ---")
        print(response)
        print("------------------------------\n")
    except Exception as e:
        print(f"Ошибка при выполнении метода run: {e}")

    print("--- Тестовый сценарий завершен ---")

if __name__ == "__main__":
    main()
