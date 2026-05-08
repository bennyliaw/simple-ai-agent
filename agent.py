import os
import json
import anthropic
from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS, OPENAI_TOOLS, TOOL_MAP

load_dotenv()

# MODEL = "claude-opus-4-7"

# no tools support
# MODEL = "deepseek-r1:1.5b"
# MODEL = "gemma3:1b-it-q4_K_M"

# support tools but wrong format
# MODEL = "qwen2.5-coder:3b"

# workable
# MODEL = "qwen2.5:7b-instruct"     # works well for slow
# MODEL = "qwen2.5:1.5b-instruct-q4_K_M" # recommended for my ollama local, support tool, and relatively fast for this
# MODEL = "qwen2.5:1.5b"  # workable, acceptable speed
# MODEL = "granite4.1:3b" # best

DEFAULT_MODEL = "granite4.1:3b"
DEFAULT_BACKEND = "openai"
SUPPORTED_MODELS = [
    "granite4.1:3b",            # fast and good
    "qwen2.5:1.5b",             # fast reasonable
    "qwen2.5:1.5b-instruct-q4_K_M", # relatively fast, sometimes not smart
    "qwen3.5:4b",               # quite slow
    "lfm2.5-thinking:1.2b",     # medium speed, very thorough
    "nemotron-3-nano:4b",       # also quite slow
    "ministral-3:3b",           # medium speed
]
SUPPORTED_BACKENDS = ["anthropic", "openai"]


def _run_anthropic(user_message: str, verbose: bool, model: str, temperature: float | None) -> str:
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": user_message}]

    kwargs = dict(model=model, max_tokens=4096, tools=TOOLS, messages=messages)
    if temperature is not None:
        kwargs["temperature"] = temperature

    while True:
        response = client.messages.create(**kwargs)

        if response.stop_reason == "end_turn":
            for block in response.content:
                if block.type == "text":
                    return block.text
            return ""

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if verbose:
                    print(f"(verbose) {block}")
                if block.type == "tool_use":
                    tool_fn = TOOL_MAP.get(block.name)
                    result = tool_fn(block.input) if tool_fn else f"Unknown tool: {block.name}"
                    print(f"[tool] {block.name}({block.input}) -> {result}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            messages.append({"role": "user", "content": tool_results})

        else:
            raise RuntimeError(f"Unexpected stop_reason: {response.stop_reason}")


def _run_openai(user_message: str, verbose: bool, model: str, temperature: float | None) -> str:
    base_url = os.environ.get("OPENAI_BASE_URL", "http://localhost:11434/v1")
    api_key = os.environ.get("OPENAI_API_KEY", "ollama")
    client = OpenAI(base_url=base_url, api_key=api_key)
    messages = [{"role": "user", "content": user_message}]

    kwargs = dict(model=model, tools=OPENAI_TOOLS, messages=messages)
    if temperature is not None:
        kwargs["temperature"] = temperature

    while True:
        response = client.chat.completions.create(**kwargs)
        choice = response.choices[0]

        if choice.finish_reason == "stop":
            return choice.message.content or ""

        if choice.finish_reason == "tool_calls":
            messages.append(choice.message)
            for tool_call in choice.message.tool_calls:
                if verbose:
                    print(f"(verbose) {tool_call}")
                name = tool_call.function.name
                input_args = json.loads(tool_call.function.arguments)
                tool_fn = TOOL_MAP.get(name)
                result = tool_fn(input_args) if tool_fn else f"Unknown tool: {name}"
                print(f"[tool] {name}({input_args}) -> {result}")
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

        else:
            raise RuntimeError(f"Unexpected finish_reason: {choice.finish_reason}")


def run(user_message: str, verbose: bool = False, model: str = None, temperature: float = None, backend: str = None) -> str:
    resolved_model = model or DEFAULT_MODEL
    resolved_backend = backend or DEFAULT_BACKEND

    if resolved_backend == "anthropic":
        return _run_anthropic(user_message, verbose, resolved_model, temperature)
    else:
        return _run_openai(user_message, verbose, resolved_model, temperature)
