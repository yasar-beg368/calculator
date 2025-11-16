from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def calculate_expression(expr):
    # Manual evaluation (simple support: +, -, *, /)
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

    return result

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
