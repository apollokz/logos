# logos/integrations/llamaindex.py

from llama_index.core.base.response.schema import Response
from llama_index.core.query_engine import CustomQueryEngine
from logos.client import Client

_logos_client = Client(llm_provider="offline", api_key="DUMMY")
# ИЗМЕНЕНИЕ: Загружаем все наборы правил из директории
_logos_client.load_ruleset("rulesets")

class LogosQueryEngine(CustomQueryEngine):
    """
    Интеграция "Логос" в качестве кастомного Query Engine для LlamaIndex.
    """
    def custom_query(self, query_str: str) -> Response:
        response_str = _logos_client.run(query_str)
        return Response(response=response_str)
