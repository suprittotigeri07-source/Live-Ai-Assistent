import ast
import operator

from app.tools.base import BaseTool


class CalculatorTool(BaseTool):

    name = "calculator"

    description = "Performs arithmetic calculations."

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
    }

    def run(self, expression: str):

        try:
            expression = expression.strip()

            if not expression:
                raise ValueError("Expression cannot be empty.")

            tree = ast.parse(expression, mode="eval")

            return self.evaluate(tree.body)

        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero.")

        except (SyntaxError, ValueError, TypeError):
            raise ValueError(
                f"Invalid arithmetic expression: {expression}"
            )

    def evaluate(self, node):

        # Numbers
        if isinstance(node, ast.Constant):

            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Only numbers are allowed.")

        # Binary operations
        if isinstance(node, ast.BinOp):

            if type(node.op) not in self.operators:
                raise ValueError("Operator not allowed.")

            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            operation = self.operators[type(node.op)]

            return operation(left, right)

        # Unary + and -
        if isinstance(node, ast.UnaryOp):

            if isinstance(node.op, ast.USub):
                return -self.evaluate(node.operand)

            if isinstance(node.op, ast.UAdd):
                return self.evaluate(node.operand)

        raise ValueError("Invalid expression.")