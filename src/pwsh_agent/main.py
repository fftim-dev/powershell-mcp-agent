from . import ollama_chat
from .tools import register_tools

def main():
    register_tools()
    ollama_chat.start()

if __name__ == "__main__":
    main()