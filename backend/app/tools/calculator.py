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
        return self.evaluate(ast.parse(expression, mode="eval").body)

    def evaluate(self, node):

        if isinstance(node, ast.Constant):
            return node.value

        if isinstance(node, ast.BinOp):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            return self.operators[type(node.op)](left, right)

        raise ValueError("Invalid expression")