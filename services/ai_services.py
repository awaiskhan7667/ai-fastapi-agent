from openai import OpenAI
from config import settings
from services.tools import get_weather, calculator
import json

client = OpenAI(api_key=settings.openai_api_key)

weather_tool = {
    "type": "function",
    "name": "get_weather",
    "description": "Get the current weather for a city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The name of the city."
            }
        },
        "required": ["city"]
    }
}
calculator_tool = {
    "type": "function",
    "name": "calculator",
    "description": "Perform a mathematical calculation.",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {
                "type": "number",
                "description": "The first number."
            },
            "b": {
                "type": "number",
                "description": "The second number."
            },
            "operation": {
                "type": "string",
                "enum": [
                    "add",
                    "subtract",
                    "multiply",
                    "divide"
                ],
                "description": "The mathematical operation."
            }
        },
        "required": ["a", "b", "operation"]
    }
}


def ask_with_tool(question: str):
    response = client.responses.create(
        model="gpt-5-mini",
        input=question,
        tools=[
            weather_tool,
            calculator_tool
        ]
    )

    while True:
        tool_outputs = []

        for item in response.output:

            if item.type == "function_call":

                arguments = json.loads(item.arguments)

                if item.name == "get_weather":
                    result = get_weather(
                        arguments["city"]
                    )

                elif item.name == "calculator":
                    result = calculator(
                        arguments["a"],
                        arguments["b"],
                        arguments["operation"]
                    )

                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result)
                })

        if not tool_outputs:
            return response.output_text

        response = client.responses.create(
            model="gpt-5-mini",
            input=tool_outputs,
            previous_response_id=response.id,
            tools=[
                weather_tool,
                calculator_tool
            ]
        )