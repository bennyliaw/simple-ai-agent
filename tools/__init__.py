from tools import calculator, clock

TOOLS = [calculator.SCHEMA, clock.SCHEMA]
OPENAI_TOOLS = [calculator.OPENAI_SCHEMA, clock.OPENAI_SCHEMA]

TOOL_MAP = {
    "calculator": calculator.run,
    "get_current_time": clock.run,
}
