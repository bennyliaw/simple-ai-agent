# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A simple Python project demonstrating an LLM-powered agent with tool use. The agent calls Claude (via the Anthropic SDK) and can invoke tools such as a calculator and a clock.
The project should be managed with `uv`.

## Shell

Prefer Git Bash over PowerShell for terminal commands.

## Setup

```bash
uv sync
```

## Running

```bash
uv run python main.py
```

## Running Tests

```bash
uv run pytest
# Single test:
uv run pytest tests/test_tools.py::test_calculator
```

## Architecture

- `main.py` — entry point; runs the agent loop
- `agent.py` — core agent logic: sends messages to the LLM, handles tool_use responses, dispatches to tools, and loops until the model returns a final text response
- `tools/` — one file per tool, each exporting a tool schema (for the API) and a `run(input)` function
- `tools/calculator.py` — evaluates arithmetic expressions
- `tools/clock.py` — returns the current date/time
- `tools/__init__.py` — collects all tool schemas and a dispatch map used by the agent

## Tool Pattern

Each tool module must export:
- `SCHEMA` — an Anthropic tool definition dict (`name`, `description`, `input_schema`)
- `run(input: dict) -> str` — executes the tool and returns a string result

The agent in `agent.py` uses the `tools` list for the API call and the `TOOL_MAP` dict to dispatch `tool_use` blocks by name.

## Backends

Two API backends are supported, selectable via `-b`:

| Backend | Description | Default base URL |
|---------|-------------|-----------------|
| `openai` | OpenAI-compatible (default) | `http://localhost:11434/v1` (Ollama) |
| `anthropic` | Anthropic Messages API | — |

Override the OpenAI base URL via `OPENAI_BASE_URL` env var. Override the API key via `OPENAI_API_KEY` (defaults to `"ollama"` for local use).

## Supported Models

| Model | Notes |
|-------|-------|
| `granite4.1:3b` | Default — fast and good |
| `qwen2.5:1.5b` | Fast, reasonable |
| `qwen2.5:1.5b-instruct-q4_K_M` | Relatively fast, sometimes not smart |
| `qwen3.5:4b` | Quite slow |
| `lfm2.5-thinking:1.2b` | Medium speed, very thorough |
| `nemotron-3-nano:4b` | Also quite slow |
| `ministral-3:3b` | Medium speed |

Use `-m <model>` to select. Use `-t <0.0-1.0>` to set temperature. Use `-b <backend>` to select backend.

## Key Dependencies

- `anthropic` — Anthropic Python SDK (Claude API)
- `pytest` — testing
