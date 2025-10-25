# examples/run_langchain_agent.py

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from logos.integrations.langchain import logos_solver_tool

# --- Конфигурация ---
# os.environ["GOOGLE_API_KEY"] = "AIza..."

def main():
    print("--- Демонстрация работы агента LangChain с Gemini и инструментом 'Логос' ---")

    try:
        # ИЗМЕНЕНИЕ: Используем точное имя модели из списка доступных
        llm = ChatGoogleGenerativeAI(model="gemini-pro-latest", temperature=0, convert_system_message_to_human=True)
    except Exception as e:
        print(f"\n[ОШИБКА] Не удалось инициализировать LLM. Убедитесь, что GOOGLE_API_KEY установлен.")
        print(f"Детали: {e}")
        return

    tools = [logos_solver_tool]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Ты — полезный ассистент. У тебя есть доступ к специальному инструменту 'logos_solver_tool' для любых задач, требующих точных вычислений или логики."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    print("\n--- Запуск: Алгебраическая задача ---")
    query = "У меня есть уравнение: 3*x - y == 5. Мне нужно найти целочисленное решение, где x > 0 и y > 0. Можешь помочь?"
    
    try:
        response = agent_executor.invoke({"input": query})
        print("\n--- Финальный ответ агента ---")
        print(response.get("output"))
        print("---------------------------------")
    except Exception as e:
        print(f"\n[ОШИБКА] Произошла ошибка во время выполнения агента.")
        print(f"Детали: {e}")

if __name__ == "__main__":
    main()
