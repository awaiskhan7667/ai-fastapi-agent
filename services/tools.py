def get_weather(city: str):
    return {
        "city": city,
        "temperature": "25°C",
        "condition": "Sunny"
    }

def calculator(a: float, b: float, operation: str):
    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        if b == 0:
            return "Cannot divide by zero"

        return a / b

    return "Invalid operation"