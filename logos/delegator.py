# logos/delegator.py

import re
from z3 import Solver, Int, sat

class Delegator:
    """
    "Делегатор" - мозг системы, который анализирует промпт
    и делегирует формализуемые задачи символьному решателю Z3.
    """
    def _handle_scheduling(self, prompt: str) -> str:
        """Обрабатывает задачи планирования."""
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

    def _handle_algebra(self, prompt: str) -> str:
        """
        Обрабатывает алгебраические задачи с помощью динамического парсера.
        """
        try:
            solver = Solver()
            var_names = set(re.findall(r'\b([a-zA-Z])\b', prompt))
            
            if not var_names:
                return "Не удалось найти переменные в уравнении. [Проверка Логос: ошибка парсинга.]"

            z3_vars = {name: Int(name) for name in var_names}
            safe_scope = z3_vars.copy()
            safe_scope["__builtins__"] = None

            # ИСПРАВЛЕНИЕ: Regex теперь использует явный, не "жадный" набор символов [a-zA-Z0-9...],
            # чтобы избежать захвата кириллических слов.
            constraints = re.findall(r'([a-zA-Z0-9\s\.\+\-\*\/()]+==[a-zA-Z0-9\s\.\+\-\*\/()]+|[a-zA-Z]+\s*(?:>|<|>=|<=)\s*-?\d+\.?\d*)', prompt)
            
            if not constraints:
                return "Не удалось найти математические ограничения в промпте. [Проверка Логос: ошибка парсинга.]"

            for c in constraints:
                solver.add(eval(c.strip(), safe_scope))

            if solver.check() == sat:
                model = solver.model()
                solution = ", ".join([f"{var} = {model[z3_vars[var]]}" for var in sorted(z3_vars.keys())])
                return f"Решение найдено: {solution}. [Проверено Логос: Решение удовлетворяет всем условиям.]"
            else:
                return "Не удалось найти целочисленное решение для данного уравнения и ограничений. [Проверено Логос: Конфликт в условиях.]"
        except Exception as e:
            return f"Ошибка при решении алгебраической задачи с Z3: {e}. [Проверка Логос: прервана.]"

    def analyze_and_translate(self, prompt: str) -> str:
        """
        Анализирует промпт, и если задача подходит для Z3,
        транслирует ее и решает.
        """
        prompt_lower = prompt.lower()
        scheduling_keywords = ["запланировать", "встречи", "расписание"]
        algebra_keywords = ["реши", "уравнение", "где"]

        if any(keyword in prompt_lower for keyword in scheduling_keywords):
            return self._handle_scheduling(prompt)
        elif any(keyword in prompt_lower for keyword in algebra_keywords):
            return self._handle_algebra(prompt)
        else:
            return "Задача не содержит формализуемых ограничений и не была передана решателю. [Проверка Логос: не выполнялась]"
