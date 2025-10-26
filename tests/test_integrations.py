# tests/test_integrations.py

from logos.integrations.langchain import logos_solver_tool
from logos.integrations.llamaindex import LogosQueryEngine

def test_langchain_tool_invocation():
    response = logos_solver_tool.invoke({"query": "Реши уравнение 3*x - y == 5, где x > 0 и y > 0."})
    assert "Решение найдено: x = 2, y = 1" in response

def test_langchain_tool_description():
    normalized_description = " ".join(logos_solver_tool.description.split())
    assert "математически доказуемую точность" in normalized_description
    assert "решения уравнений" in normalized_description

def test_llamaindex_query_engine_invocation():
    query_engine = LogosQueryEngine()
    prompt = "Если Алиса идет на вечеринку, то Боб не идет. Если Клара не идет, то Алиса идет. Клара точно не пойдет."
    
    # ИСПРАВЛЕНИЕ: Вызываем `custom_query` вместо `query`
    response = query_engine.custom_query(prompt)
    
    assert "Алиса = True" in response.response
    assert "Боб = False" in response.response
