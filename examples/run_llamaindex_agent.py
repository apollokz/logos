# examples/run_llamaindex_agent.py

from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI  # Для примера используем OpenAI
from logos.integrations.llamaindex import LogosQueryEngine
import os

# --- Конфигурация ---
# Установите ваш OpenAI API ключ
# os.environ["OPENAI_API_KEY"] = "sk-..."

def main():
    print("--- Демонстрация работы агента LlamaIndex с инструментом 'Логос' ---")

    try:
        # Для простоты демонстрации мы будем использовать LLM от OpenAI.
        # В реальном приложении здесь может быть любая LLM, совместимая с LlamaIndex.
        llm = OpenAI(model="gpt-3.5-turbo")
    except Exception as e:
        print(f"\n[ОШИБКА] Не удалось инициализировать LLM. Убедитесь, что OPENAI_API_KEY установлен.")
        print(f"Детали: {e}")
        return

    # 1. Создаем экземпляр нашего Query Engine
    logos_query_engine = LogosQueryEngine()

    # 2. "Оборачиваем" наш Query Engine в Tool, чтобы агент мог его использовать
    # Мы даем ему имя и четкое описание, чтобы LLM понимала, для чего он нужен.
    logos_tool = QueryEngineTool.from_defaults(
        query_engine=logos_query_engine,
        name="logos_solver",
        description=(
            "Используй этот инструмент для решения любых задач, требующих строгой логики, "
            "математических вычислений, решения уравнений, булевой логики или проверки "
            "данных по набору правил. Этот инструмент обеспечивает математически "
            "доказуемую точность."
        ),
    )

    # 3. Создаем ReAct агента, передав ему наш инструмент
    agent = ReActAgent.from_tools([logos_tool], llm=llm, verbose=True)

    print("\n--- Запуск: Алгебраическая задача ---")
    query = "У меня есть уравнение: 3*x - y == 5. Мне нужно найти целочисленное решение, где x > 0 и y > 0. Можешь помочь?"

    try:
        response = agent.chat(query)
        print("\n--- Финальный ответ агента ---")
        print(response)
        print("---------------------------------")
    except Exception as e:
        print(f"\n[ОШИБКА] Произошла ошибка во время выполнения агента.")
        print(f"Детали: {e}")


if __name__ == "__main__":
    main()
k
