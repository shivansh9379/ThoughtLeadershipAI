import math


def calculate(expression: str):
    try:
        expression = expression.replace("^", "**")

        allowed = {
            "__builtins__": None,
            "abs": abs,
            "round": round,
            "pow": pow,
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "pi": math.pi,
            "e": math.e,
        }

        result = eval(expression, allowed, {})

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }