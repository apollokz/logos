# logos/integrations/langchain.py

from langchain.tools import tool
from logos.client import Client

# Мы создаем один глобальный экземпляр клиента, чтобы не инициализировать его при каждом вызове.
# В более сложных приложениях здесь может использоваться более продвинутый паттерн.
_logos_client = Client(llm_provider="offline", api_key="DUMMY")
_logos_client.load_ruleset(name="compliance", filepath="compliance_rules.json")

@tool
def logos_solver_tool(query: str) -> str:
    """
    Используй этот инструмент для решения любых задач, требующих строгой логики,
    математических вычислений, решения уравнений, булевой логики или проверки
    данных по набору правил. Этот инструмент обеспечивает математически
    доказуемую точность.
    """
    return _logos_client.run(query)
