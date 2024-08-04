from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Default values
initial_capital = 5000
target_gain_percentage = 0.10  # 10%
number_of_trades = 5
win_percentage = 0.85  # 85%

# Sample data for demonstration purposes
trades = []

def calculate_risk_amount(initial_capital, target_gain_percentage, number_of_trades, win_percentage):
    target_profit = initial_capital * target_gain_percentage
    required_profit_per_trade = target_profit / number_of_trades
    risk_amount = required_profit_per_trade / win_percentage
    return risk_amount

risk_amount = calculate_risk_amount(initial_capital, target_gain_percentage, number_of_trades, win_percentage)

@app.route('/')
def index():
    global initial_capital, risk_amount
    total_trades = len(trades)
    current_capital = initial_capital + sum(trade['profit_loss'] for trade in trades)
    risk_amount = calculate_risk_amount(current_capital, target_gain_percentage, number_of_trades, win_percentage) if current_capital > 0 else 0
    return render_template('index.html', initial_capital=initial_capital, total_trades=total_trades, trades=trades, current_capital=current_capital, risk_amount=risk_amount)

@app.route('/set_initial_capital', methods=['POST'])
def set_initial_capital():
    global initial_capital, risk_amount
    initial_capital = float(request.form['initial_capital'])
    risk_amount = calculate_risk_amount(initial_capital, target_gain_percentage, number_of_trades, win_percentage)
    return redirect(url_for('index'))

@app.route('/submit_trade', methods=['POST'])
def submit_trade():
    global risk_amount
    result = request.form['result']
    amount = risk_amount
    profit_loss = amount * win_percentage if result == 'Win' else -amount
    trades.append({'result': result, 'amount': amount, 'profit_loss': profit_loss})
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    global trades, risk_amount, initial_capital
    trades = []
    risk_amount = calculate_risk_amount(initial_capital, target_gain_percentage, number_of_trades, win_percentage)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
