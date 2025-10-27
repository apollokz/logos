# logos/client.py

import os
import json
from pathlib import Path
from .delegator import Delegator

class Client:
    """
    Основной клиент для взаимодействия с системой "Логос".
    """
    def __init__(self, llm_provider: str, api_key: str):
        self.llm_provider = llm_provider
        self.api_key = api_key
        self.rulesets = {}
        self.delegator = Delegator(self)
        print("Клиент Логос и Делегатор успешно инициализированы.")

    def load_ruleset(self, path: str):
        """
        Улучшенный метод для загрузки набора правил из файла или директории.
        """
        p = Path(path)
        if not p.exists():
            print(f"Ошибка: Путь '{path}' не существует.")
            return

        if p.is_file() and p.suffix == '.json':
            # Загрузка одного файла
            ruleset_name = p.stem  # Имя файла без расширения
            self.rulesets[ruleset_name] = str(p)
            print(f"Набор правил '{ruleset_name}' из файла '{p}' успешно загружен.")
        elif p.is_dir():
            # Загрузка всех .json файлов из директории
            count = 0
            for json_file in p.glob('*.json'):
                ruleset_name = json_file.stem
                self.rulesets[ruleset_name] = str(json_file)
                print(f"Набор правил '{ruleset_name}' из файла '{json_file}' успешно загружен.")
                count += 1
            print(f"Загружено {count} наборов правил из директории '{p}'.")

    def run(self, prompt: str) -> str:
        print(f"Получен промпт: '{prompt}'")
        response = self.delegator.analyze_and_translate(prompt)
        return response
