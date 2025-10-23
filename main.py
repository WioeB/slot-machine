from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

balance = 100
symbols = ["🍓", "🍋", "🥝", "🍒", "🍇"]

def tirada():
    return random.choices(symbols, k=3)

def check(resultado, bet):
    if resultado[0] == resultado[1] == resultado[2]:
        return bet * 3, "You won!"
    else:
        return -bet, "You lost!"

@app.route("/", methods=["GET", "POST"])
def index():
    global balance
    message = ""
    resultado = []

    if request.method == "POST":
        try:
            apuesta = int(request.form["bet"])
            if apuesta <= 0:
                message = "Bet must be greater than 0."
            elif apuesta > balance:
                message = "You don't have enough balance."
            else:
                resultado = tirada()
                ganancias, message = check(resultado, apuesta)
                balance += ganancias
        except ValueError:
            message = "Please enter a valid number."

    return render_template("index.html", balance=balance, resultado=resultado, message=message)

@app.route("/add_funds", methods=["POST"])
def add_funds():
    global balance
    balance += 1
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)