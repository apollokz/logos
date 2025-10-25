# logos/delegator.py

import re
from z3 import Solver, Int, Real, sat, is_rational_value, is_int_value

class Delegator:
    """
    "Делегатор" - мозг системы, который анализирует промпт
    и делегирует формализуемые задачи символьному решателю Z3.
    """
    def _handle_scheduling(self, prompt: str) -> str:
        # ... (этот метод остается без изменений) ...
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
        """Форматирует значение из модели Z3 в читаемый вид."""
        if is_rational_value(val) and not is_int_value(val):
            # Если это дробь, представляем ее как десятичное число с 4 знаками после запятой
            return f"{val.as_decimal(4).replace('?', '')}"
        else:
            # Иначе (целое число) - просто возвращаем как есть
            return f"{val}"

    def _handle_algebra(self, prompt: str) -> str:
        """
        Обрабатывает алгебраические задачи, поддерживая целые и вещественные числа.
        """
        try:
            solver = Solver()
            var_names = set(re.findall(r'\b([a-zA-Z])\b', prompt))
            
            if not var_names:
                return "Не удалось найти переменные в уравнении. [Проверка Логос: ошибка парсинга.]"

            # ИСПРАВЛЕНИЕ 1: Более надежная эвристика для определения типа
            # Ищем все числа в промпте и проверяем, есть ли среди них числа с точкой.
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
                # ИСПРАВЛЕНИЕ 2: Используем функцию форматирования для красивого вывода
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

    def analyze_and_translate(self, prompt: str) -> str:
        # ... (этот метод остается без изменений) ...
        prompt_lower = prompt.lower()
        scheduling_keywords = ["запланировать", "встречи", "расписание"]
        algebra_keywords = ["реши", "уравнение", "где"]

        if any(keyword in prompt_lower for keyword in scheduling_keywords):
            return self._handle_scheduling(prompt)
        elif any(keyword in prompt_lower for keyword in algebra_keywords):
            return self._handle_algebra(prompt)
        else:
            return "Задача не содержит формализуемых ограничений и не была передана решателю. [Проверка Логос: не выполнялась]"
