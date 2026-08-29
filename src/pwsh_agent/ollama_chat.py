from ollama import chat
from .tools.base import Tool
from .config import PROMPTS_DIR

def get_system_prompt():
    try:
        with open(str(PROMPTS_DIR / "system.md"), "r", encoding="utf-8") as file:
            system_prompt = file.read()
    except FileNotFoundError:
        system_prompt = ""
    return system_prompt


def start():
    chat_history = [
        {"role": "system", "content": get_system_prompt()}
    ]

    while True:
        readLine = input("You: ")
        if readLine == "exit":
            break

        chat_history.append({"role": "user", "content": readLine})
        ollama_reponse = get_ollama_response(chat_history)
        print(ollama_reponse)


def get_ollama_response(chat_history):
    response = chat(
        model="ornith-1.5:9b",
        messages=chat_history,
        tools=Tool.get_ollama_tools()
    )

    if not response.done:
        raise Exception("Response not completed")

    chat_history.append(response.message)
    tool_calls = response.message.tool_calls

    if not tool_calls:
        return response.message.content
    
    handle_tool_response(tool_calls, chat_history)
    return get_ollama_response(chat_history)


def handle_tool_response(tool_calls, chat_history):
    if not tool_calls:
        return
    
    for tool_call in tool_calls:
        tool = Tool.get(tool_call.function.name)
        result = tool.execute(**tool_call.function.arguments)

        chat_history.append({
            "role": "tool",
            "tool_name": tool_call.function.name,
            "content": result.json
        })