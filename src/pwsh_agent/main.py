from .ollama.chat import start
from .tools import register_tools

def main():
    register_tools()
    start()

if __name__ == "__main__":
    main()