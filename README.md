# Logos: A Symbolic Coprocessor for LLMs

Logos is a symbolic coprocessor for Large Language Models (LLMs) that replaces probabilistic reasoning with verifiable, mathematical guarantees using the Z3 solver. It acts as a truth guarantor for your most critical AI tasks.

## Key Features

*   **Algebraic Solver**: Dynamically parse and solve algebraic equations with integer and real numbers.
*   **Boolean Logic Solver**: Solve classic boolean satisfiability (SAT) problems.
*   **Rule Engine**: Validate data against a user-defined set of rules loaded from an external JSON file.

## Installation

Install the official package from PyPI:

```bash
pip install logos-solver
```

## Quick Start Examples

### Example 1: Algebraic Solver

Create a file `example_algebra.py`:

```python
from logos.client import Client

logos_client = Client(llm_provider="openai", api_key="DUMMY_API_KEY")

prompt = "Реши уравнение 3*x - y == 5, где x > 0 и y > 0."
response = logos_client.run(prompt)
print(response)
```
**Output:**
```
Решение найдено: x = 2, y = 1. [Проверено Логос: Решение удовлетворяет всем условиям.]
```

### Example 2: Boolean Logic Solver

Create a file `example_boolean.py`:
```python
from logos.client import Client

logos_client = Client(llm_provider="openai", api_key="DUMMY_API_KEY")

prompt = "Если Алиса идет на вечеринку, то Боб не идет. Если Клара не идет, то Алиса идет. Клара точно не пойдет. Кто в итоге пойдет на вечеринку?"
response = logos_client.run(prompt)
print(response)
```
**Output:**
```
Решение найдено: Алиса = True, Боб = False, Клара = False. [Проверено Логос: Вывод логически корректен.]
```

### Example 3: Rule Engine

First, create a `rules.json` file:
```json
{
  "description": "Compliance rules for transactions",
  "rules": [
    "amount < 10000",
    "risk_score <= 0.85"
  ]
}
```
Now, create `example_rules.py`:
```python
from logos.client import Client

logos_client = Client(llm_provider="openai", api_key="DUMMY_API_KEY")

# This transaction is valid
valid_prompt = "Проверь транзакцию с amount=9500 risk_score=0.7 по набору правил 'rules.json'"
print(f"Valid case: {logos_client.run(valid_prompt)}")

# This transaction is invalid
invalid_prompt = "Проверь транзакцию с amount=12000 risk_score=0.5 по набору правил 'rules.json'"
print(f"Invalid case: {logos_client.run(invalid_prompt)}")
```
**Output:**
```
Valid case: Проверка пройдена. Все 2 правила из 'rules.json' выполнены. [Проверено Логос: Соответствие подтверждено.]
Invalid case: Проверка провалена. Данные нарушают одно или несколько правил из 'rules.json'. [Проверено Логос: Обнаружено несоответствие.]
```
```
