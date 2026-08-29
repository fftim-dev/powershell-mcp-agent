from . import Tool
from . import filesystem

def register_tools():
    Tool(
        "list_files", 
        "List files in a directory", 
        {
            "type": "object", 
            "properties": {
                "path": {
                    "type": "string"
                }
            },
            "required": ["path"]
        }, 
        filesystem.list_files)

    Tool(
        "list_directory",
        "List all files and directories in a directory",
        {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string"
                }
            },
            "required": ["path"]
        },
        filesystem.list_directory)
    
    Tool(
        "get_current_directory", 
        "Get the current working directory", 
        {
            "type": "object", 
            "properties": {}
        }, 
        filesystem.get_current_directory
    )
    
    Tool(
        "find_files", 
        "Find files in a directory matching a pattern", 
        {
            "type": "object", 
            "properties": {
                "path": {
                    "type": "string"
                },
                "pattern": {
                    "type": "string"
                },
                "limit": {
                    "type": "integer"
                }
            },
            "required": ["path", "pattern"]
        }, 
        filesystem.find_files
    )