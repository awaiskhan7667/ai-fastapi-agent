from typing import TypedDict, Any

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from config import settings
from langgraph.graph import StateGraph, START, END

from services.tools import get_weather, calculator


# -------------------------
# Tools
# -------------------------

@tool
def weather(city: str):
    """Get the weather for a city."""
    return get_weather(city)


@tool
def calculate(a: float, b: float, operation: str):
    """Perform a mathematical calculation."""
    return calculator(a, b, operation)


# -------------------------
# LLM
# -------------------------

llm = ChatOpenAI(
    model="gpt-5-mini",
    api_key=settings.openai_api_key
)

tools = [weather, calculate]

llm_with_tools = llm.bind_tools(tools)


# -------------------------
# State
# -------------------------

class AgentState(TypedDict):
    question: str
    answer: str
    messages: list[Any]


# -------------------------
# LLM Node
# -------------------------

def answer_node(state: AgentState):

    response = llm_with_tools.invoke(
        state["question"]
    )

    return {
        "answer": response.content,
        "messages": [response]
    }


# -------------------------
# Tool Node
# -------------------------

def tool_node(state: AgentState):

    message = state["messages"][-1]

    tool_calls = message.tool_calls

    results = []

    for call in tool_calls:

        if call["name"] == "weather":

            result = weather.invoke(
                call["args"]
            )

        elif call["name"] == "calculate":

            result = calculate.invoke(
                call["args"]
            )

        results.append(str(result))

    return {
        "answer": "\n".join(results)
    }


# -------------------------
# Final Answer Node
# -------------------------

def final_answer_node(state: AgentState):

    response = llm.invoke(
        f"""
Answer the user's question using this tool result.

Question:
{state["question"]}

Tool result:
{state["answer"]}
"""
    )

    return {
        "answer": response.content
    }


# -------------------------
# Router
# -------------------------

def route_after_llm(state: AgentState):

    message = state["messages"][-1]

    if message.tool_calls:
        return "tool"

    return "end"


# -------------------------
# Create Graph
# -------------------------

graph = StateGraph(AgentState)


# Nodes
graph.add_node("answer", answer_node)
graph.add_node("tool", tool_node)
graph.add_node("final_answer", final_answer_node)

# Start
graph.add_edge(
    START,
    "answer"
)

# LLM decides:
# Tool or normal answer
graph.add_conditional_edges(
    "answer",
    route_after_llm,
    {
        "tool": "tool",
        "end": END
    }
)

# Tool → Final LLM answer
graph.add_edge(
    "tool",
    "final_answer"
)

# Final answer → END
graph.add_edge(
    "final_answer",
    END
)

# Compile
app = graph.compile()

# -------------------------
# Test
# -------------------------
# result = app.invoke({
#     "question": "What is the weather in Lahore and what is 25 multiplied by 4?",
#     "answer": "",
#     "messages": []
# })
# print(result)

test_cases = [
    {
        "question": "What is 25 multiplied by 4?",
        "expected": "100"
    },
    {
        "question": "What is 10 plus 5?",
        "expected": "15"
    },
    {
    "question": "What is the weather in Lahore?",
    "expected": "Lahore"
    },
    {
    "question": "What is 50 divided by 0?",
    "expected": "Cannot divide by zero"
    }
]

def evaluate_answer(actual, expected):
    if expected.lower() in actual.lower():
        return "PASS"
    return "FAIL"



passed = 0

for test in test_cases:
    result = app.invoke({
        "question": test["question"],
        "answer": "",
        "messages": []
    })

    score = evaluate_answer(
        result["answer"],
        test["expected"]
    )

    if score == "PASS":
        passed += 1

    print("Question:", test["question"])
    print("Result:", score)

accuracy = passed / len(test_cases) * 100

print(f"Accuracy: {accuracy}%")