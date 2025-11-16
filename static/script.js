let expr = "";

function press(value) {
    expr += value;
    document.getElementById("display").value = expr;
}

function clearDisplay() {
    expr = "";
    document.getElementById("display").value = "";
}

function calculate() {
    fetch("/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ expression: expr })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("display").value = data.result;
        expr = data.result.toString();
    });
}
