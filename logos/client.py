# logos/client.py

from .delegator import Delegator

class Client:
    """
    Основной клиент для взаимодействия с системой "Логос".
    """
    def __init__(self, llm_provider: str, api_key: str):
        self.llm_provider = llm_provider
        self.api_key = api_key
        # ИЗМЕНЕНИЕ: Добавляем хранилище для наборов правил
        self.rulesets = {}
        # ИЗМЕНЕНИЕ: Передаем ссылку на самого себя в Делегатор
        self.delegator = Delegator(self)
        print("Клиент Логос и Делегатор успешно инициализированы.")

    def load_ruleset(self, name: str, filepath: str):
        """
        ИЗМЕНЕНИЕ: Новый метод для загрузки набора правил из файла.
        """
        # В будущем здесь может быть более сложная валидация
        self.rulesets[name] = filepath
        print(f"Набор правил '{name}' из файла '{filepath}' успешно загружен.")

    def run(self, prompt: str) -> str:
        print(f"Получен промпт: '{prompt}'")
        response = self.delegator.analyze_and_translate(prompt)
        return response
