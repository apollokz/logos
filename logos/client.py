# logos/client.py

from .delegator import Delegator # <-- ИЗМЕНЕНИЕ: Импортируем наш новый компонент

class Client:
    """
    Основной клиент для взаимодействия с системой "Логос".

    Этот класс абстрагирует сложность взаимодействия с LLM и символьным
    решателем, предоставляя единый, простой в использовании интерфейс.
    """
    def __init__(self, llm_provider: str, api_key: str):
        """
        Инициализирует клиент "Логос" и его компоненты.

        Args:
            llm_provider (str): Название провайдера LLM (например, "openai").
            api_key (str): API ключ для доступа к сервисам LLM.
        """
        self.llm_provider = llm_provider
        self.api_key = api_key
        # ИЗМЕНЕНИЕ: Создаем экземпляр Делегатора при инициализации клиента
        self.delegator = Delegator()
        print("Клиент Логос и Делегатор успешно инициализированы.")

    def run(self, prompt: str) -> str:
        """
        Основной метод для обработки запроса пользователя.

        Args:
            prompt (str): Запрос пользователя на естественном языке.

        Returns:
            str: Ответ, сгенерированный системой.
        """
        print(f"Получен промпт: '{prompt}'")
        # ИЗМЕНЕНИЕ: Заменяем заглушку на вызов реального Делегатора
        response = self.delegator.analyze_and_translate(prompt)
        return response
