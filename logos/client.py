# logos/logos/client.py
import os
import json
import re 
from z3 import Solver, Real, And, Or, sat

class Client:
    def __init__(self, llm_provider="offline", api_key="DUMMY"):
        self.rulesets = {}

    def load_ruleset(self, directory="rulesets"):
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                ruleset_name = filename.split(".")[0]
                with open(os.path.join(directory, filename), "r") as f:
                    self.rulesets[ruleset_name] = json.load(f)["rules"]

    def _parse_prompt(self, prompt: str):
        """
        Используем надежный парсинг с помощью регулярных выражений.
        Это будет находить все пары 'переменная=значение'.
        """
        constraints = {}
        pattern = re.compile(r"(\w+)\s*=\s*([0-9.]+)")
        matches = pattern.findall(prompt)

        for name, value in matches:
            try:
                constraints[name] = float(value)
            except ValueError:
                pass
        return constraints

    def run(self, prompt: str, ruleset_name="compliance"):
        print(f"Получен промпт: '{prompt}'") 

        constraints = self._parse_prompt(prompt)

        # ИЗМЕНЕНИЕ 1: Всегда возвращаем словарь для консистентности API
        if not constraints:
            return {
                "result": "no_op",
                "details": "Задача не содержит формализуемых ограничений и не была передана решателю.",
                "triggered_rules": []
            }

        s = Solver()
        variables = {name: Real(name) for name in constraints.keys()}

        for name, value in constraints.items():
            s.add(variables[name] == value)

        rules_to_check = self.rulesets.get(ruleset_name, [])
        if not rules_to_check:
            return {
                "result": "error",
                "details": f"Набор правил '{ruleset_name}' не найден.",
                "triggered_rules": []
            }

        # ИЗМЕНЕНИЕ 2: Создаем список для хранения успешно примененных правил
        triggered_rules = []
        try:
            for rule_str in rules_to_check:
                rule_expr = eval(rule_str, {"__builtins__": None}, variables)
                s.add(rule_expr)
                # Если правило успешно добавлено, фиксируем его
                triggered_rules.append(rule_str)
        except Exception as e:
            return {
                "result": "error",
                "details": f"Ошибка при парсинге правила: {e}.",
                "triggered_rules": triggered_rules # Возвращаем даже частично сработавшие
            }

        # ИЗМЕНЕНИЕ 3: Возвращаем структурированный ответ
        if s.check() == sat:
            return {
                "result": "approved",
                "details": "Все правила успешно верифицированы.",
                "triggered_rules": triggered_rules
            }
        else:
            return {
                "result": "denied",
                "details": "Одно или несколько правил не были выполнены.",
                "triggered_rules": triggered_rules
            }
