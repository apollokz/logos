# logos/integrations/llamaindex.py

from llama_index.core.base.response.schema import Response
# ИСПРАВЛЕНИЕ: Используем единственно верный путь, найденный в ходе диагностики
from llama_index.core.query_engine import CustomQueryEngine
from logos.client import Client

_logos_client = Client(llm_provider="offline", api_key="DUMMY")
_logos_client.load_ruleset(name="compliance", filepath="compliance_rules.json")

class LogosQueryEngine(CustomQueryEngine):
    """
    Интеграция "Логос" в качестве кастомного Query Engine для LlamaIndex.
    """
    def custom_query(self, query_str: str) -> Response:
        response_str = _logos_client.run(query_str)
        return Response(response=response_str)
