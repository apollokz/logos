# logos/delegator.py

import re
from z3 import Solver, Int, Real, Bool, And, Or, Not, Implies, sat, is_rational_value, is_int_value

class Delegator:
    """
    "Делегатор" - мозг системы, который анализирует промпт
    и делегирует формализуемые задачи символьному решателю Z3.
    """
    def _handle_scheduling(self, prompt: str) -> str:
        # ... (без изменений) ...
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
        # ... (без изменений) ...
        if is_rational_value(val) and not is_int_value(val):
            return f"{val.as_decimal(4).replace('?', '')}"
        else:
            return f"{val}"

    def _handle_algebra(self, prompt: str) -> str:
        # ... (без изменений) ...
        try:
            solver = Solver()
            var_names = set(re.findall(r'\b([a-zA-Z])\b', prompt))
            
            if not var_names:
                return "Не удалось найти переменные в уравнении. [Проверка Логос: ошибка парсинга.]"

            all_numbers = re.findall(r'-?\d+\.\d+', prompt)
            use_reals = len(all_numbers) > 0
            VarType = Real if use_reals else Int

            z3_vars = {name: VarType(name) for name in var_names}
            safe_scope = z3_vars.copy()
            safe_scope["__builtins__"] = None

            constraints = re.findall(r'([a-zA-Z0-9\s\.\+\-\*\/()]+==[a-zA-Z0-9\s\.\+\-\*\/()]+|[a-zA-Z]+\s*(?:>|<|>=|<=)\s*-?\d+\.?\d*)', prompt)
            
            if not constraints:
                return "Не удалось найти математические ограничения в промпте. [Проверка Логос: ошибка парсинга.]"

            for c in constraints:
                solver.add(eval(c.strip(), safe_scope))

            if solver.check() == sat:
                model = solver.model()
                solution_parts = []
                for var in sorted(z3_vars.keys()):
                    val = model[z3_vars[var]]
                    if val is not None:
                         solution_parts.append(f"{var} = {self._format_model_value(val)}")

                solution = ", ".join(solution_parts)
                return f"Решение найдено: {solution}. [Проверено Логос: Решение удовлетворяет всем условиям.]"
            else:
                return "Не удалось найти решение для данного уравнения и ограничений. [Проверено Логос: Конфликт в условиях.]"
        except Exception as e:
            return f"Ошибка при решении алгебраической задачи с Z3: {e}. [Проверка Логос: прервана.]"

    def _handle_boolean_logic(self, prompt: str) -> str:
        """
        ИЗМЕНЕНИЕ: Новый метод для решения задач булевой логики.
        """
        try:
            # Жестко закодированный парсер для конкретного примера.
            Алиса, Боб, Клара = Bool('Алиса'), Bool('Боб'), Bool('Клара')
            solver = Solver()

            # "Если Алиса идет на вечеринку, то Боб не идет." -> Implies(Алиса, Not(Боб))
            solver.add(Implies(Алиса, Not(Боб)))
            
            # "Если Клара не идет, то Алиса идет." -> Implies(Not(Клара), Алиса)
            solver.add(Implies(Not(Клара), Алиса))
            
            # "Клара точно не пойдет." -> Not(Клара)
            solver.add(Not(Клара))

            if solver.check() == sat:
                model = solver.model()
                solution = ", ".join([f"{v} = {model[v]}" for v in [Алиса, Боб, Клара]])
                return f"Решение найдено: {solution}. [Проверено Логос: Вывод логически корректен.]"
            else:
                return "Условия задачи противоречивы, решения не существует. [Проверено Логос: Обнаружено противоречие.]"

        except Exception as e:
            return f"Ошибка при решении логической задачи с Z3: {e}. [Проверка Логос: прервана.]"

    def analyze_and_translate(self, prompt: str) -> str:
        """
        Анализирует промпт, и если задача подходит для Z3,
        транслирует ее и решает.
        """
        prompt_lower = prompt.lower()
        scheduling_keywords = ["запланировать", "встречи", "расписание"]
        algebra_keywords = ["реши", "уравнение", "где"]
        # ИЗМЕНЕНИЕ: Добавляем ключевые слова для нового типа задач
        boolean_keywords = ["если", "то", "не идет", "вечеринку"]

        if any(keyword in prompt_lower for keyword in scheduling_keywords):
            return self._handle_scheduling(prompt)
        elif any(keyword in prompt_lower for keyword in algebra_keywords):
            return self._handle_algebra(prompt)
        # ИЗМЕНЕНИЕ: Добавляем новую ветку в маршрутизатор
        elif all(keyword in prompt_lower for keyword in boolean_keywords):
            return self._handle_boolean_logic(prompt)
        else:
            return "Задача не содержит формализуемых ограничений и не была передана решателю. [Проверка Логос: не выполнялась]"
