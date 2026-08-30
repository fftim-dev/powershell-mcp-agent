from . import filesystem
from .base import Tool

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

    Tool(
        "read_file",
        "Read the contents of a single file",
        {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string"
                }
        },
        "required": ["path"]
        },
        filesystem.read_file
    )

    Tool(
        "read_files",
        "Read the contents of multiple files",
        {
            "type": "object",
            "properties": {
                "paths": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["paths"]
        },
        filesystem.read_files
    )