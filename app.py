from flask import Flask, render_template, request, jsonify
import math
import ast
import operator as op
app = Flask(__name__)



def eval_expr(expr):
    node = ast.parse(expr, mode='eval').body
    return eval_(node)

def eval_(node):
    if isinstance(node, ast.Num):  # numbers
        return node.n

    elif isinstance(node, ast.BinOp):  # binary operations (+-*/)
        left = eval_(node.left)
        right = eval_(node.right)
        return operators[type(node.op)](left, right)

    elif isinstance(node, ast.UnaryOp):  # -3, +5
        operand = eval_(node.operand)
        return operators[type(node.op)](operand)

    else:
        raise TypeError("Invalid expression")


def calculate_expression(expr):
    # Manual evaluation (simple support: +, -, *, /)
    # Handle log function manually
    if expr.startswith("log(") and expr.endswith(")"):
        num = float(expr[4:-1])  # extract number inside parentheses
        return math.log10(num)   # base-10 log

    if expr.startswith("√"):
        num = float(expr[1:])
        return math.sqrt(num)
    numbers = []
    operators = []
    current = ""

    for char in expr:
        if char.isdigit() or char == ".":
            current += char
        else:
            numbers.append(float(current))
            operators.append(char)
            current = ""

    numbers.append(float(current))

    # Now solve step-by-step
    result = numbers[0]

    for i, op in enumerate(operators):
        if op == "+":
            result += numbers[i+1]
        elif op == "-":
            result -= numbers[i+1]
        elif op == "*":
            result *= numbers[i+1]
        elif op == "/":
            if numbers[i+1] == 0:
                return "Error: Division by zero"
            result /= numbers[i+1]
        elif op == "^":
            result = result ** numbers[i+1]
    return result
# Allowed operators
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    
    data = request.json
    expression = data.get("expression", "")
    result = calculate_expression(expression)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
