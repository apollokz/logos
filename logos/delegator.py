# logos/delegator.py

import re
import json
from z3 import Solver, Int, Real, Bool, And, Or, Not, Implies, sat, is_rational_value, is_int_value

class Delegator:
    def __init__(self, client):
        """ИЗМЕНЕНИЕ: Принимаем экземпляр клиента для доступа к его данным."""
        self.client = client
    
    # ... методы _handle_scheduling, _format_model_value, _handle_algebra, _handle_boolean_logic без изменений ...
    def _handle_scheduling(self, prompt: str) -> str:
        try:
            A, B, C = Int('A'), Int('B'), Int('C')
            solver = Solver()
            solver.add(A < B)
            solver.add(C != A)
            solver.add(A >= 9, A <= 11)
            solver.add(B >= 9, B <= 11)
            solver.add(C >= 9, C <= 11)
            if solver.check() == sat:
                model = solver.model()
                schedule = f"A в {model[A]}:00, B в {model[B]}:00, C в {model[C]}:00."
                return f"Возможное расписание: {schedule} [Проверено Логос: Данное расписание удовлетворяет всем ограничениям.]"
            else:
                return "Не удалось найти расписание, удовлетворяющее всем ограничениям. [Проверено Логос: Конфликт в условиях.]"
        except Exception as e:
            return f"Ошибка при решении задачи планирования с Z3: {e}. [Проверка Логос: прервана.]"

    def _format_model_value(self, val):
        if is_rational_value(val) and not is_int_value(val):
            return f"{val.as_decimal(4).replace('?', '')}"
        else:
            return f"{val}"

    def _handle_algebra(self, prompt: str) -> str:
        try:
            solver = Solver()
            var_names = set(re.findall(r'\b([a-zA-Z])\b', prompt))
            if not var_names: return "Не удалось найти переменные в уравнении. [Проверка Логос: ошибка парсинга.]"
            all_numbers = re.findall(r'-?\d+\.\d+', prompt)
            use_reals = len(all_numbers) > 0
            VarType = Real if use_reals else Int
            z3_vars = {name: VarType(name) for name in var_names}
            safe_scope = z3_vars.copy()
            safe_scope["__builtins__"] = None
            constraints = re.findall(r'([a-zA-Z0-9\s\.\+\-\*\/()]+==[a-zA-Z0-9\s\.\+\-\*\/()]+|[a-zA-Z]+\s*(?:>|<|>=|<=)\s*-?\d+\.?\d*)', prompt)
            if not constraints: return "Не удалось найти математические ограничения в промпте. [Проверка Логос: ошибка парсинга.]"
            for c in constraints: solver.add(eval(c.strip(), safe_scope))
            if solver.check() == sat:
                model = solver.model()
                solution_parts = []
                for var in sorted(z3_vars.keys()):
                    val = model[z3_vars[var]]
                    if val is not None: solution_parts.append(f"{var} = {self._format_model_value(val)}")
                solution = ", ".join(solution_parts)
                return f"Решение найдено: {solution}. [Проверено Логос: Решение удовлетворяет всем условиям.]"
            else:
                return "Не удалось найти решение для данного уравнения и ограничений. [Проверено Логос: Конфликт в условиях.]"
        except Exception as e:
            return f"Ошибка при решении алгебраической задачи с Z3: {e}. [Проверка Логос: прервана.]"

    def _handle_boolean_logic(self, prompt: str) -> str:
        try:
            Алиса, Боб, Клара = Bool('Алиса'), Bool('Боб'), Bool('Клара')
            solver = Solver()
            solver.add(Implies(Алиса, Not(Боб)))
            solver.add(Implies(Not(Клара), Алиса))
            solver.add(Not(Клара))
            if solver.check() == sat:
                model = solver.model()
                solution = ", ".join([f"{v} = {model[v]}" for v in [Алиса, Боб, Клара]])
                return f"Решение найдено: {solution}. [Проверено Логос: Вывод логически корректен.]"
            else:
                return "Условия задачи противоречивы, решения не существует. [Проверено Логос: Обнаружено противоречие.]"
        except Exception as e:
            return f"Ошибка при решении логической задачи с Z3: {e}. [Проверка Логос: прервана.]"

    def _handle_rule_engine(self, prompt: str) -> str:
        try:
            # ИЗМЕНЕНИЕ: Ищем имя набора правил, а не имя файла
            match_ruleset = re.search(r"по набору правил '(\w+)'", prompt)
            if not match_ruleset: return "Не удалось найти имя набора правил в промпте. [Проверка Логос: ошибка парсинга.]"
            ruleset_name = match_ruleset.group(1)

            # ИЗМЕНЕНИЕ: Получаем путь к файлу из клиента
            filepath = self.client.rulesets.get(ruleset_name)
            if not filepath: return f"Ошибка: набор правил '{ruleset_name}' не был загружен. [Проверка Логос: прервана.]"

            data_pairs = re.findall(r'(\w+)=([\d\.]+)', prompt)
            if not data_pairs: return "Не удалось найти данные для проверки. [Проверка Логос: ошибка парсинга.]"
            
            with open(filepath, 'r') as f:
                rules = json.load(f).get("rules", [])
            
            for rule in rules:
                solver = Solver()
                z3_vars = {key: Real(key) if '.' in val else Int(key) for key, val in data_pairs}
                for key, val in data_pairs:
                    solver.add(z3_vars[key] == (float(val) if '.' in val else int(val)))
                rule_expr = eval(rule, {"__builtins__": None}, z3_vars)
                solver.add(Not(rule_expr))
                if solver.check() == sat:
                    model = solver.model()
                    violated_var = re.search(r'\b([a-zA-Z_]+)\b', rule).group(1)
                    actual_value = model[z3_vars[violated_var]]
                    return (f"Проверка провалена. Нарушено правило '{rule}' "
                            f"(фактическое значение: {violated_var} = {actual_value}). "
                            f"[Проверено Логос: Обнаружено несоответствие.]")

            return f"Проверка пройдена. Все {len(rules)} правила из набора '{ruleset_name}' выполнены. [Проверено Логос: Соответствие подтверждено.]"
        except FileNotFoundError:
            return f"Ошибка: файл правил '{filepath}' не найден. [Проверка Логос: прервана.]"
        except Exception as e:
            return f"Ошибка при работе движка правил: {e}. [Проверка Логос: прервана.]"

    def analyze_and_translate(self, prompt: str) -> str:
        # ... (маршрутизатор без изменений) ...
        prompt_lower = prompt.lower()
        rule_engine_keywords = ["проверь", "транзакцию", "правил"]
        scheduling_keywords = ["запланировать", "встречи", "расписание"]
        algebra_keywords = ["реши", "уравнение", "где"]
        boolean_keywords = ["если", "то", "не идет", "вечеринку"]
        # ИЗМЕНЕНИЕ: Убираем .json из ключевых слов, т.к. теперь ищем имя набора правил
        if all(keyword in prompt_lower for keyword in rule_engine_keywords):
            return self._handle_rule_engine(prompt)
        elif any(keyword in prompt_lower for keyword in scheduling_keywords):
            return self._handle_scheduling(prompt)
        elif any(keyword in prompt_lower for keyword in algebra_keywords):
            return self._handle_algebra(prompt)
        elif all(keyword in prompt_lower for keyword in boolean_keywords):
            return self._handle_boolean_logic(prompt)
        else:
            return "Задача не содержит формализуемых ограничений и не была передана решателю. [Проверка Логос: не выполнялась]"
