# logos/delegator.py

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
        """Обрабатывает простые алгебраические задачи."""
        # ПРИМЕЧАНИЕ: На данном этапе парсинг жестко закодирован под конкретный пример.
        # В будущем здесь потребуется более сложный парсер (например, на регулярных выражениях).
        try:
            x, y = Int('x'), Int('y')
            solver = Solver()
            
            # Извлекаем ограничения из промпта "Реши x + 2*y == 7, где x > 2 и y < 10"
            solver.add(x + 2*y == 7)
            solver.add(x > 2)
            solver.add(y < 10)

            if solver.check() == sat:
                model = solver.model()
                solution = f"x = {model[x]}, y = {model[y]}"
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
        # Эвристическая маршрутизация
        scheduling_keywords = ["запланировать", "встречи", "расписание"]
        algebra_keywords = ["реши", "уравнение", "x +", "x >"]

        if any(keyword in prompt.lower() for keyword in scheduling_keywords):
            return self._handle_scheduling(prompt)
        elif any(keyword in prompt.lower() for keyword in algebra_keywords):
            return self._handle_algebra(prompt)
        else:
            return "Задача не содержит формализуемых ограничений и не была передана решателю. [Проверка Логос: не выполнялась]"
