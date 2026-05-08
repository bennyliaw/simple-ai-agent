# simple-ai-agent

A minimal Python AI agent with tool use. The agent autonomously decides when to call tools, executes them, and feeds the results back to the model until it produces a final answer — no orchestration framework needed.

Supports two API backends:
- **OpenAI-compatible** — works with [Ollama](https://ollama.com) (local or remote) and any OpenAI-compatible endpoint
- **Anthropic** — works with the Anthropic Claude API or Ollama via `ANTHROPIC_BASE_URL`

## Features

- Agentic tool-use loop — model calls tools, results are fed back, loop continues until final answer
- Dual backend support: `openai` (default) and `anthropic`
- CLI flags for model, temperature, and backend
- Per-prompt and total elapsed time displayed
- Built-in tools: calculator and clock
- Easily extensible — add a new tool in one file

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) for package management
- Ollama running locally or on your network (for local models), or an Anthropic API key (for Claude)

## Setup

```bash
git clone https://github.com/bennyliaw/simple-ai-agent.git
cd simple-ai-agent

# Install dependencies
uv sync

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys / Ollama host
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | — | Anthropic API key (required for `anthropic` backend with Claude) |
| `ANTHROPIC_BASE_URL` | Anthropic cloud | Override to point to Ollama via the anthropic backend |
| `OPENAI_BASE_URL` | `http://localhost:11434/v1` | Ollama or any OpenAI-compatible endpoint |
| `OPENAI_API_KEY` | `ollama` | API key for the OpenAI-compatible backend |

## Usage

```bash
# Interactive mode (default model: granite4.1:3b, default backend: openai)
uv run python main.py

# Run built-in example prompts
uv run python main.py -E

# Select a different model
uv run python main.py -m qwen2.5:1.5b

# Use Anthropic backend
uv run python main.py -b anthropic

# Set sampling temperature
uv run python main.py -t 0.3

# Combine options
uv run python main.py -E -m qwen2.5:1.5b -b openai -t 0.5 -v
```

### CLI options

| Flag | Description |
|------|-------------|
| `-E`, `--examples` | Run built-in example prompts instead of interactive mode |
| `-m`, `--model` | Model to use (see supported models below) |
| `-b`, `--backend` | API backend: `openai` (default) or `anthropic` |
| `-t`, `--temperature` | Sampling temperature, 0.0–1.0 |
| `-v`, `--verbose` | Print raw tool call blocks for debugging |

### Example output

```
Simple LLM Agent Demo — granite4.1:3b [openai]
========================================

User: What is 123 * 456 + 789?
[tool] calculator({'expression': '123 * 456 + 789'}) -> 56877
Agent: The result is 56,877.
[2.41s]

User: What time is it right now?
[tool] get_current_time({}) -> 2026-05-08 01:37:43 UTC
Agent: The current time (UTC) is 2026-05-08 01:37:43.
[1.83s]

========================================
Total time: 4.24s
```

## Supported Models

These models are tested with Ollama and support tool use:

| Model | Notes |
|-------|-------|
| `granite4.1:3b` | Default — fast and good |
| `qwen2.5:1.5b` | Fast, reasonable |
| `qwen2.5:1.5b-instruct-q4_K_M` | Relatively fast, sometimes not smart |
| `qwen3.5:4b` | Quite slow |
| `lfm2.5-thinking:1.2b` | Medium speed, very thorough |
| `nemotron-3-nano:4b` | Also quite slow |
| `ministral-3:3b` | Medium speed |

## Architecture

```
main.py          — CLI entry point, argument parsing, output formatting
agent.py         — core agent loop; _run_anthropic() and _run_openai() backends
tools/
  __init__.py    — collects TOOLS, OPENAI_TOOLS, and TOOL_MAP
  calculator.py  — evaluates arithmetic expressions safely via AST
  clock.py       — returns current UTC date/time
tests/
  test_tools.py  — tool unit tests
  test_main.py   — CLI argument validation tests
```

## Adding a Tool

1. Create `tools/mytool.py` exporting `SCHEMA`, `OPENAI_SCHEMA`, and `run(input: dict) -> str`
2. Import and register it in `tools/__init__.py`

```python
# tools/mytool.py
SCHEMA = {
    "name": "my_tool",
    "description": "Does something useful.",
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
    },
}

OPENAI_SCHEMA = {
    "type": "function",
    "function": {
        "name": "my_tool",
        "description": SCHEMA["description"],
        "parameters": SCHEMA["input_schema"],
    },
}

def run(input: dict) -> str:
    return f"Result for: {input['query']}"
```

## Running Tests

```bash
uv run pytest
uv run pytest -v          # verbose
uv run pytest tests/test_tools.py::test_calculator_addition   # single test
```

## License

MIT
