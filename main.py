import argparse
import sys
import time
import agent
from agent import run

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXAMPLES = [
    "What is 123 * 456 + 789?",
    "What time is it right now?",
    "If I have 1000 dollars and spend 37.5% of it, how much do I have left?",
    # "There were 216 red and green marbles in a box. After 30% of the red marbles and 50% of the green marbles were given away, an equal number of green and red marbles were left. How many red marbles were in the box at first?",
]


def temperature_arg(value):
    try:
        f = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"temperature must be a number, got '{value}'")
    if not 0.0 <= f <= 1.0:
        raise argparse.ArgumentTypeError(f"temperature must be between 0.0 and 1.0, got {value}")
    return f


def _model_temp_label(model: str, temperature: float | None) -> str:
    label = model
    if temperature is not None:
        label += f" (temp={temperature})"
    return label


def _header_label(model: str, temperature: float | None, backend: str) -> str:
    label = _model_temp_label(model, temperature)
    return f"{label} [{backend}]"


def run_examples(verbose: bool, model: str, temperature: float | None, backend: str):
    print(f"Simple LLM Agent Demo — {_header_label(model, temperature, backend)}\n" + "=" * 40)
    total_start = time.perf_counter()
    for prompt in EXAMPLES:
        print(f"\nUser: {prompt}")
        t0 = time.perf_counter()
        answer = run(prompt, verbose=verbose, model=model, temperature=temperature, backend=backend)
        elapsed = time.perf_counter() - t0
        print(f"Agent: {answer}")
        print(f"[{elapsed:.2f}s]")
    total_elapsed = time.perf_counter() - total_start
    print(f"\n{'=' * 40}\nTotal time: {total_elapsed:.2f}s")


def run_interactive(verbose: bool, model: str, temperature: float | None, backend: str):
    print(f"Simple LLM Agent (interactive) [{_header_label(model, temperature, backend)}] — type 'exit' or Ctrl-C to quit\n" + "=" * 40)
    while True:
        try:
            prompt = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not prompt or prompt.lower() in {"exit", "quit"}:
            break
        t0 = time.perf_counter()
        answer = run(prompt, verbose=verbose, model=model, temperature=temperature, backend=backend)
        elapsed = time.perf_counter() - t0
        print(f"Agent: {answer}")
        print(f"[{elapsed:.2f}s]")


def main():
    parser = argparse.ArgumentParser(description="Simple LLM Agent")
    parser.add_argument("-E", "--examples", action="store_true", help="Run built-in example prompts instead of interactive mode")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print tool call inputs and outputs")
    parser.add_argument("-m", "--model", choices=agent.SUPPORTED_MODELS, default=agent.DEFAULT_MODEL, help="Model to use (default: %(default)s)")
    parser.add_argument("-t", "--temperature", type=temperature_arg, default=None, metavar="[0.0-1.0]", help="Sampling temperature between 0.0 and 1.0")
    parser.add_argument("-b", "--backend", choices=agent.SUPPORTED_BACKENDS, default=agent.DEFAULT_BACKEND, help="API backend to use (default: %(default)s)")
    args = parser.parse_args()

    if args.examples:
        run_examples(verbose=args.verbose, model=args.model, temperature=args.temperature, backend=args.backend)
    else:
        run_interactive(verbose=args.verbose, model=args.model, temperature=args.temperature, backend=args.backend)


if __name__ == "__main__":
    main()
