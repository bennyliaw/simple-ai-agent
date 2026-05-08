import ast
import operator

SCHEMA = {
    "name": "calculator",
    "description": "Evaluate a simple arithmetic expression. Supports +, -, *, /, ** and parentheses.",
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Arithmetic expression to evaluate, e.g. '2 + 3 * (4 - 1)'",
            }
        },
        "required": ["expression"],
    },
}

OPENAI_SCHEMA = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": SCHEMA["description"],
        "parameters": SCHEMA["input_schema"],
    },
}

_SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _SAFE_OPS:
        return _SAFE_OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _SAFE_OPS:
        return _SAFE_OPS[type(node.op)](_eval(node.operand))
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def run(input: dict) -> str:
    expr = input["expression"]
    try:
        tree = ast.parse(expr, mode="eval")
        result = _eval(tree.body)
        return str(result)
    except Exception as e:
        return f"Error: {e}"
