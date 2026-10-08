# from xmlrpc import client

from openai import OpenAI
from config import settings

client = OpenAI(api_key=settings.openai_api_key)


def ask_ai(question: str, history: list[dict]):
    try:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Give clear and concise answers."
            }
        ]

        messages.extend(history)

        messages.append({
            "role": "user",
            "content": question
        })

        response = client.responses.create(
            model="gpt-5-mini",
            input=messages
        )

        return {
            "question": question,
            "answer": response.output_text
        }

    except Exception as e:
        return {
            "question": question,
            "answer": f"AI service error: {str(e)}"
        }


def stream_ai(question: str):
    response = client.responses.create(
        model="gpt-5-mini",
        input=question,
        stream=True
    )

    for event in response:
        if event.type == "response.output_text.delta":
            yield event.delta    