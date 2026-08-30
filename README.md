# PowerShell MCP Agent

An experimental MCP server and local Ollama agent that delegate deterministic filesystem work to PowerShell and return structured results to the language model.

The project is currently a small, read-only tool layer for Windows. Its reusable core is a shared tool registry and PowerShell execution layer; GitHub Copilot can consume the tools through MCP, while a local Ollama agent can call the same tools directly.

## Why this project exists

Language models are useful for deciding **what operation is needed** and interpreting its result. They do not need to perform every deterministic filesystem operation themselves or reason over an entire repository when a focused local query can provide the relevant data.

This project explores the hypothesis that pairing small, lightweight local models with deterministic PowerShell tools can:

- move filesystem and command-line work onto the local machine;
- return focused structured data instead of unnecessary context;
- reduce token use and duplicated repository exploration;
- reduce hallucinations about filesystem and system state;
- make smaller local models more useful in agentic workflows;
- support agents with narrow roles and limited toolsets; and
- make future multi-agent workflows more efficient by assigning specialized responsibilities.

For example, a repository-analysis agent could be responsible only for locating and reading files. Other agents would receive its relevant findings instead of independently exploring the same repository or loading it in full.

These are research goals, not measured results. The repository does not yet contain benchmarks demonstrating token, latency, or quality improvements.

## Core idea

The model chooses an operation and supplies its arguments. A local PowerShell script performs the deterministic work, and the Python layer returns the decoded output in a common result envelope:

```text
Model: decide what to inspect
              |
              v
Tool: perform a narrow local operation
              |
              v
Model: interpret the structured result
```

This keeps repository exploration separate from model reasoning. The current tools only inspect the filesystem; they do not create, edit, move, or delete files.

## Architecture

GitHub Copilot uses the stdio MCP server:

```text
GitHub Copilot
      |
      v
     MCP
      |
      v
 Tool Registry
      |
      v
 PowerShell
      |
      v
Structured Result
```

The local agent bypasses MCP but uses the same registry and execution functions:

```text
Local Ollama Agent
        |
        v
  Tool Registry
        |
        v
   PowerShell
        |
        v
 Structured Result
```

The registry is the single source of truth for each tool's name, description, JSON input schema, and Python execution function. The MCP server intentionally uses the lower-level `mcp.server.Server` API to expose registry entries through `list_tools` and dispatch calls through `call_tool`, rather than defining a second set of MCP-specific tools.

The execution path is:

```text
Client -> registry entry -> Python wrapper -> packaged .ps1 script
       <- JSON result    <- result adapter <- PowerShell output
```

PowerShell processes run with `-NoProfile`. The runner applies timeouts, caps captured standard output, and reports the exit code and whether output was truncated.

## Current features

- stdio MCP server for local clients such as GitHub Copilot in VS Code;
- six read-only filesystem tools;
- one shared registry for MCP and Ollama tool definitions;
- packaged PowerShell scripts for deterministic filesystem operations;
- JSON-decoded tool content in a common success/error envelope;
- PowerShell execution timeouts and output truncation metadata; and
- an interactive local Ollama agent using a fixed model configuration.

Current limitations are important:

- The runner invokes the Windows `powershell` executable, so the current implementation targets Windows PowerShell on Windows.
- Tools are not restricted to the current workspace. They can read any path accessible to the operating-system user running the server.
- There are no write/edit tools, workspace security policies, automated tests, or benchmarks yet.
- The MCP transport is stdio only; there is no HTTP or REST server.

## Available tools

| Tool | Arguments | Behavior |
| --- | --- | --- |
| `get_current_directory` | none | Returns the server process's current working directory. |
| `list_files` | `path: string` | Lists files immediately inside a directory; it is not recursive. |
| `list_directory` | `path: string` | Lists immediate child files and directories. |
| `find_files` | `path: string`, `pattern: string`, optional `limit: integer` | Recursively finds files using a PowerShell filter. The default limit is 50. |
| `read_file` | `path: string` | Reads one complete file as text. |
| `read_files` | `paths: string[]` | Reads multiple complete files as text in one tool call. |

Paths may be absolute or relative to the server process's current directory. `get_current_directory` can be used to determine that base directory.

Every known tool returns a JSON string with this shape through MCP and Ollama:

```json
{
  "status": "success",
  "content": {},
  "error": null,
  "meta": {
    "exit_code": 0,
    "truncated": false
  }
}
```

`content` contains the JSON value emitted by the relevant PowerShell script, so its exact shape depends on the operation. Failed execution uses `status: "error"`, sets `content` to `null`, and includes an error message.

## Installation

Requirements:

- Windows with the `powershell` command available;
- Python 3.11 or later; and
- [`pipx`](https://pipx.pypa.io/) for an isolated, globally available CLI installation.

Install the project directly from GitHub:

```powershell
git clone https://github.com/fftim-dev/powershell-mcp-agent.git
cd powershell-mcp-agent
pipx install .
```

`pipx` installs the package and its Python dependencies into an isolated environment, then exposes its CLI commands globally. After installation, `pwsh-mcp` can be used from any other VS Code project; it does not need to run from the cloned repository.

The installed MCP entry point is:

```powershell
pwsh-mcp
```

Running it starts a stdio server. It normally waits silently for an MCP client; it is not an interactive shell command.

## GitHub Copilot and VS Code MCP setup

After installing the project with `pipx`, open any VS Code project where Copilot should use the tools and create `.vscode/mcp.json` in that project:

```json
{
  "servers": {
    "powershell-mcp-agent": {
      "type": "stdio",
      "command": "pwsh-mcp"
    }
  }
}
```

Then:

1. Open the workspace in VS Code.
2. Start or restart `powershell-mcp-agent` from the `mcp.json` editor or run **MCP: List Servers** from the Command Palette.
3. Confirm that you trust the server when VS Code prompts you. The tools inherit your user account's filesystem access.
4. Open GitHub Copilot Chat in Agent mode.
5. Open the tools picker and enable the `powershell-mcp-agent` tools if they are not already enabled.
6. Ask Copilot to inspect files in the workspace.

See the [VS Code MCP configuration reference](https://code.visualstudio.com/docs/agents/reference/mcp-configuration) for current client-side configuration details.

## Usage example

Ask Copilot:

```text
Find all result.py files in this project, read their contents, and briefly explain what each file is responsible for.
```

A typical tool flow is:

```text
Copilot
  -> find_files
  -> PowerShell recursive search
  -> matching file paths
  -> read_files
  -> PowerShell file reading
  -> structured file contents
  -> final model explanation
```

PowerShell handles file discovery and reading locally. Copilot decides which operations to call and interprets only the returned files. This is the central separation the project is designed to explore.

The same tools can be requested more directly, for example:

```text
List the immediate contents of this workspace and summarize its top-level structure.
```

```text
Read pyproject.toml and tell me the package name, Python requirement, dependencies, and CLI commands.
```

## GitHub Copilot screenshots

<p align="center">
  <img src="docs/images/copilot-tools.png" alt="GitHub Copilot MCP tools" width="650">
</p>

<p align="center"><em>GitHub Copilot discovering the tools exposed by the PowerShell MCP server.</em></p>

<p align="center">
  <img src="docs/images/copilot-file-analysis.png" alt="GitHub Copilot using PowerShell MCP tools" width="650">
</p>

<p align="center"><em>Copilot invoking MCP tools to inspect the project and return a concise result.</em></p>

## Local Ollama usage

The `pwsh-agent` command starts an interactive local agent that exposes the same registry in Ollama's function-calling format.

In addition to the base requirements, run an Ollama service and install the model currently hard-coded by the project:

```powershell
ollama pull ornith-1.5:9b
pwsh-agent
```

Enter prompts at the `You:` prompt. Enter `exit` to stop the agent.

The Python `ollama` client is currently a normal package dependency, so it is installed with both `pip` and `pipx`. The Ollama service and model are separate runtime requirements. The model name is not yet configurable through a command-line option or configuration file.

## Project structure

```text
.
|-- pyproject.toml                 Package metadata, dependencies, and CLI entry points
|-- src/pwsh_agent/
|   |-- config.py                 Paths to packaged prompts and PowerShell scripts
|   |-- main.py                   Local Ollama CLI entry point
|   |-- mcp/
|   |   `-- server.py             Low-level stdio MCP server
|   |-- ollama/
|   |   `-- chat.py               Interactive Ollama tool-calling loop
|   |-- powershell/
|   |   |-- runner.py             Subprocess, timeout, and output-limit handling
|   |   |-- result.py             Raw PowerShell result type
|   |   `-- scripts/              Deterministic filesystem scripts
|   |-- prompts/
|   |   `-- system.md             Local agent system prompt
|   `-- tools/
|       |-- base.py               Tool definition and shared registry
|       |-- filesystem.py         Python-to-PowerShell adapters
|       |-- registry.py           Names, descriptions, schemas, and functions
|       `-- result.py             Public structured tool result
`-- docs/images/                  README screenshots
```

## Development setup

Clone the repository and create an isolated environment:

```powershell
git clone https://github.com/fftim-dev/powershell-mcp-agent.git
cd powershell-mcp-agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Run the MCP server from the environment:

```powershell
python -m pwsh_agent.mcp.server
```

Run the local Ollama agent:

```powershell
python -m pwsh_agent.main
```

There is currently no automated test suite. When changing a tool, keep its registry schema, Python wrapper, PowerShell script, and result serialization aligned.

## Building the package

Install the standard Python build frontend and create a source distribution and wheel:

```powershell
python -m pip install build
python -m build
```

Build artifacts are written to `dist/`, including a wheel and source distribution. This directory is generated build output and is not required for a normal installation from GitHub. PowerShell scripts and the Ollama system prompt are included as package data by `pyproject.toml`.

As an optional development or release check, install the built wheel with `pipx`:

```powershell
pipx install .\dist\<wheel-file>.whl
```

This verifies the packaged installation, including the PowerShell scripts and prompt files. It is not the primary end-user installation path.

## Roadmap

Possible next steps, none of which are implemented yet, include:

- automated tests and continuous integration;
- benchmarks for token use, latency, and output quality with and without deterministic tools;
- configurable Ollama models and agent settings;
- additional read-only inspection tools;
- carefully scoped write/edit tools;
- workspace boundaries and more advanced security policies;
- specialized roles and multi-agent orchestration;
- an HTTP/REST API with OpenAPI or Swagger documentation; and
- Docker packaging where the Windows PowerShell dependency can be addressed appropriately.

## Project status

This project is experimental and under active development. The MCP and Ollama paths are implemented and share the same six read-only tools, but the broader efficiency and multi-agent ideas remain research directions. No benchmark results should be inferred from the current implementation. The package version is maintained in `pyproject.toml`.

## License

This project is available under the [MIT License](LICENSE).
