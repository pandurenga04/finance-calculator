from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Finance Calculator</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
    body {
        margin: 0;
        padding: 0;
        background-image: url('https://www.portotheme.com/wp-content/uploads/2024/05/robot-arm-ai-analyzing-mathematics-mechanized-industry-problem-solving.webp');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        font-family: Arial, sans-serif;
    }
    .container {
        background: rgba(0, 0, 0, 0.8); /* Adjusted darker overlay */
        padding: 20px;
        border-radius: 10px;
        width: 100%;
        max-width: 600px;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.5);
    }
    h1 {
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }
    .btn {
        margin-bottom: 15px;
    }
    form {
        color: white;
    }
    #calculator-container h3 {
        text-align: center;
        margin-top: 20px;
        color: #00ff00; /* Green color for the result */
    }
</style>

        </head>
        <body>
            <div class="container">
                <h1>Finance Calculator</h1>
                <button class="btn btn-primary w-100" onclick="showCalculator('si')">Simple Interest</button>
                <button class="btn btn-success w-100" onclick="showCalculator('ci')">Compound Interest</button>
                <button class="btn btn-warning w-100" onclick="showCalculator('emi')">EMI</button>
                <button class="btn btn-info w-100" onclick="showCalculator('roi')">ROI</button>
                <button class="btn btn-secondary w-100" onclick="showCalculator('basic')">Basic Calculator</button>

                <div id="calculator-container" class="mt-4"></div>
            </div>

            <script>
                async function showCalculator(type) {
                    const response = await fetch(`/${type}`);
                    const html = await response.text();
                    document.getElementById('calculator-container').innerHTML = html;
                }

                async function submitForm(event, type) {
                    event.preventDefault();
                    const form = event.target;
                    const formData = new FormData(form);
                    const response = await fetch(`/${type}`, {
                        method: 'POST',
                        body: formData
                    });
                    const result = await response.json();
                    document.getElementById(`${type}-result`).innerHTML = `<h3>Result: ${result.result}</h3>`;
                }
            </script>
        </body>
        </html>
    '''

@app.route('/si', methods=['GET', 'POST'])
def simple_interest():
    if request.method == 'POST':
        principal = float(request.form['principal'])
        rate = float(request.form['rate'])
        time = float(request.form['time'])
        si = (principal * rate * time) / 100
        return jsonify(result=f"Simple Interest = {si}")
    return '''
        <h2>Simple Interest Calculator</h2>
        <form onsubmit="submitForm(event, 'si')">
            <div>
                Principal: <input type="number" name="principal" class="form-control" required><br>
                Rate of Interest: <input type="number" name="rate" class="form-control" required><br>
                Time (in years): <input type="number" name="time" class="form-control" required><br>
            </div>
            <button type="submit" class="btn btn-primary mt-2">Calculate</button>
        </form>
        <div id="si-result" class="mt-4"></div>
    '''

@app.route('/ci', methods=['GET', 'POST'])
def compound_interest():
    if request.method == 'POST':
        principal = float(request.form['principal'])
        rate = float(request.form['rate'])
        time = float(request.form['time'])
        ci = principal * ((1 + rate / 100) ** time) - principal
        return jsonify(result=f"Compound Interest = {ci}")
    return '''
        <h2>Compound Interest Calculator</h2>
        <form onsubmit="submitForm(event, 'ci')">
            <div>
                Principal: <input type="number" name="principal" class="form-control" required><br>
                Rate of Interest: <input type="number" name="rate" class="form-control" required><br>
                Time (in years): <input type="number" name="time" class="form-control" required><br>
            </div>
            <button type="submit" class="btn btn-success mt-2">Calculate</button>
        </form>
        <div id="ci-result" class="mt-4"></div>
    '''

@app.route('/emi', methods=['GET', 'POST'])
def emi():
    if request.method == 'POST':
        principal = float(request.form['principal'])
        rate = float(request.form['rate']) / (12 * 100)  # Monthly interest rate
        tenure = int(request.form['tenure'])  # Tenure in months
        emi = (principal * rate * ((1 + rate) ** tenure)) / (((1 + rate) ** tenure) - 1)
        return jsonify(result=f"EMI = {emi}")
    return '''
        <h2>EMI Calculator</h2>
        <form onsubmit="submitForm(event, 'emi')">
            <div>
                Loan Amount: <input type="number" name="principal" class="form-control" required><br>
                Rate of Interest: <input type="number" name="rate" class="form-control" required><br>
                Tenure (in months): <input type="number" name="tenure" class="form-control" required><br>
            </div>
            <button type="submit" class="btn btn-warning mt-2">Calculate</button>
        </form>
        <div id="emi-result" class="mt-4"></div>
    '''

@app.route('/roi', methods=['GET', 'POST'])
def roi():
    if request.method == 'POST':
        investment = float(request.form['investment'])
        return_amount = float(request.form['return_amount'])
        roi = ((return_amount - investment) / investment) * 100
        return jsonify(result=f"ROI = {roi}%")
    return '''
        <h2>ROI Calculator</h2>
        <form onsubmit="submitForm(event, 'roi')">
            <div>
                Investment: <input type="number" name="investment" class="form-control" required><br>
                Return Amount: <input type="number" name="return_amount" class="form-control" required><br>
            </div>
            <button type="submit" class="btn btn-info mt-2">Calculate</button>
        </form>
        <div id="roi-result" class="mt-4"></div>
    '''

@app.route('/basic', methods=['GET', 'POST'])
def basic_calculator():
    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operation = request.form['operation']
        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            result = num1 / num2 if num2 != 0 else "Error (Division by Zero)"
        return jsonify(result=f"Result = {result}")
    return '''
        <h2>Basic Calculator</h2>
        <form onsubmit="submitForm(event, 'basic')">
            <div>
                Number 1: <input type="number" name="num1" class="form-control" required><br>
                Number 2: <input type="number" name="num2" class="form-control" required><br>
                Operation:
                <select name="operation" class="form-select">
                    <option value="add">Addition</option>
                    <option value="subtract">Subtraction</option>
                    <option value="multiply">Multiplication</option>
                    <option value="divide">Division</option>
                </select><br>
            </div>
            <button type="submit" class="btn btn-secondary mt-2">Calculate</button>
        </form>
        <div id="basic-result" class="mt-4"></div>
    '''

if __name__ == '__main__':
    app.run(debug=True)
