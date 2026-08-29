class Tool:
    registry = {}
    
    def __init__(self, name, description, input_schema, execute):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.execute = execute
        Tool.registry[self.name] = self

    def to_ollama(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_schema
            }
        }

    @staticmethod
    def get(name):
        return Tool.registry.get(name)
    
    @staticmethod
    def get_ollama_tools():
        return [
            tool.to_ollama()
            for tool in Tool.registry.values()
        ]