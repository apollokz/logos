# logos/delegator.py

import re
import json
from z3 import Solver, Int, Real, Bool, And, Or, Not, Implies, sat, is_rational_value, is_int_value

class Delegator:
    def __init__(self, client):
        self.client = client
    
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
            var_names = set(re.findall(r'\b([А-ЯЁ][а-яё]+)\b', prompt))
            if not var_names:
                return "Не удалось найти переменные (имена) в задаче. [Проверка Логос: ошибка парсинга.]"

            solver = Solver()
            z3_vars = {name: Bool(name) for name in var_names}
            
            processed_prompt = prompt
            var_pattern = f"({'|'.join(var_names)})"

            processed_prompt = re.sub(f"{var_pattern}\\s+не\\s+идет", r"Not(\1)", processed_prompt)
            processed_prompt = re.sub(f"{var_pattern}\\s+точно\\s+не\\s+пойдет", r"Not(\1)", processed_prompt)
            processed_prompt = re.sub(f"{var_pattern}\\s+идет(\\s+на\\s+вечеринку)?", r"\1", processed_prompt)
            
            safe_scope = z3_vars.copy()
            safe_scope.update({'Implies': Implies, 'Not': Not})
            safe_scope["__builtins__"] = None

            found_constraints = False
            implications = re.findall(r'Если\s+(.*?),\s*то\s+(.*?)\.', processed_prompt, flags=re.IGNORECASE)
            for cond, conclusion in implications:
                solver.add(Implies(eval(cond.strip(), safe_scope), eval(conclusion.strip(), safe_scope)))
                found_constraints = True

            remaining_text = re.sub(r'Если\s+(.*?),\s*то\s+(.*?)\.', '', processed_prompt, flags=re.IGNORECASE)
            facts = [f.strip() for f in remaining_text.split('.') if f.strip()]
            for fact in facts:
                if fact.startswith("Not(") and fact.endswith(")"):
                    solver.add(eval(fact, safe_scope))
                    found_constraints = True
            
            if not found_constraints:
                return "Не удалось найти логические ограничения в промпте. [Проверка Логос: ошибка парсинга.]"

            if solver.check() == sat:
                model = solver.model()
                solution_parts = []
                # --- ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ ---
                # Итерируемся по переменным в модели и используем правильный синтаксис model[var]
                # Сортируем по имени для стабильного вывода
                sorted_decls = sorted(model.decls(), key=lambda d: d.name())
                for d in sorted_decls:
                    solution_parts.append(f"{d.name()} = {model[d]}")

                solution = ", ".join(solution_parts)
                return f"Решение найдено: {solution}. [Проверено Логос: Вывод логически корректен.]"
            else:
                return "Условия задачи противоречивы, решения не существует. [Проверено Логос: Обнаружено противоречие.]"
        except Exception as e:
            return f"Ошибка при решении логической задачи с Z3: {e}. [Проверка Логос: прервана.]"

    def _build_rule_expr(self, rule_str, z3_vars):
        parts = rule_str.split()
        if len(parts) != 3: return None
        var_name, op, value_str = parts
        if var_name not in z3_vars: return None
        z3_var = z3_vars[var_name]
        value = float(value_str) if '.' in value_str else int(value_str)
        if op == '<': return z3_var < value
        if op == '>': return z3_var > value
        if op == '<=': return z3_var <= value
        if op == '>=': return z3_var >= value
        if op == '==': return z3_var == value
        if op == '!=': return z3_var != value
        return None

    def _handle_rule_engine(self, prompt: str) -> str:
        try:
            match_ruleset = re.search(r"по набору правил '(\w+)'", prompt)
            if not match_ruleset: return "Не удалось найти имя набора правил."
            ruleset_name = match_ruleset.group(1)

            filepath = self.client.rulesets.get(ruleset_name)
            if not filepath: return f"Ошибка: набор правил '{ruleset_name}' не загружен."

            data_map = {}
            keyword_map = {'на сумму': 'amount', 'с оценкой риска': 'risk_score', 'в час': 'transaction_hour'}
            for phrase, var_name in keyword_map.items():
                match = re.search(f"{phrase}\\s+([\\d\\.]+)", prompt)
                if match:
                    data_map[var_name] = match.group(1)
            
            if not data_map: return "Не удалось найти данные для проверки в промпте."
            
            with open(filepath, 'r') as f:
                rules = json.load(f).get("rules", [])
            
            solver = Solver()
            z3_vars = {key: Real(key) if '.' in val else Int(key) for key, val in data_map.items()}
            for key, val in data_map.items():
                solver.add(z3_vars[key] == (float(val) if '.' in val else int(val)))

            for rule in rules:
                rule_expr = self._build_rule_expr(rule, z3_vars)
                if rule_expr is None:
                    continue

                solver.push()
                solver.add(Not(rule_expr))

                if solver.check() == sat:
                    model = solver.model()
                    violated_var_name = rule.split()[0]
                    actual_value = model.eval(z3_vars[violated_var_name], model_completion=True)
                    solver.pop()
                    return (f"Проверка провалена. Нарушено правило '{rule}' "
                            f"(фактическое значение: {violated_var_name} = {self._format_model_value(actual_value)}). "
                            f"[Проверено Логос: Обнаружено несоответствие.]")
                
                solver.pop()

            return f"Проверка пройдена. Все применимые правила из набора '{ruleset_name}' выполнены. [Проверено Логос: Соответствие подтверждено.]"
        except Exception as e:
            return f"Ошибка при работе движка правил: {e}. [Проверка Логос: прервана.]"

    def analyze_and_translate(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        rule_engine_keywords = ["проверь", "транзакцию", "правил"]
        scheduling_keywords = ["запланировать", "встречи", "расписание"]
        algebra_keywords = ["реши", "уравнение", "где"]
        boolean_keywords = ["если", "то", "не идет", "вечеринку"]
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
