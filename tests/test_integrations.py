# tests/test_integrations.py

from logos.integrations.langchain import logos_solver_tool

def test_langchain_tool_invocation():
    """
    Проверяет, что инструмент LangChain правильно вызывает ядро Логоса
    и возвращает корректный результат для алгебраической задачи.
    """
    response = logos_solver_tool.invoke({"query": "Реши уравнение 3*x - y == 5, где x > 0 и y > 0."})
    
    assert "Решение найдено: x = 2, y = 1" in response

def test_langchain_tool_description():
    """Проверяет, что у инструмента есть правильное описание для LLM."""
    # ИЗМЕНЕНИЕ: Нормализуем описание, заменяя все пробельные символы (включая \n)
    # на обычные пробелы. Это делает тест нечувствительным к форматированию.
    normalized_description = " ".join(logos_solver_tool.description.split())
    
    assert "математически доказуемую точность" in normalized_description
    assert "решения уравнений" in normalized_description # Добавим еще одну проверку для надежности
