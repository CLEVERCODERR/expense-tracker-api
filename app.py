from flask import Flask, jsonify, request, render_template
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "data.json"

#load expenses from JSON
def load_expenses():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("expenses", [])
    except FileNotFoundError:
        return []

#save expenses to JSON
def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump({"expenses": expenses}, f, indent=4)

#frontend route
@app.route("/")
def index():
    return render_template("index.html")

#get all expenses
@app.route("/expenses", methods=["GET"])
def get_expenses():
    expenses = load_expenses()
    return jsonify(expenses), 200

#add a new expense
@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()
    required_fields = ["amount", "category"]

    #validate input
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing amount or category"}), 400

    expense = {
        "amount": data["amount"],
        "category": data["category"],
        "description": data.get("description", ""),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    expenses = load_expenses()
    expenses.append(expense)
    save_expenses(expenses)

    return jsonify(expense), 201

#total expenses
@app.route("/expenses/total", methods=["GET"])
def total_expenses():
    expenses = load_expenses()
    total = sum(e["amount"] for e in expenses)
    return jsonify({"total_expenses": total}), 200

#summary by category
@app.route("/expenses/summary", methods=["GET"])
def summary_by_category():
    expenses = load_expenses()
    summary = {}
    for e in expenses:
        summary[e["category"]] = summary.get(e["category"], 0) + e["amount"]
    return jsonify(summary), 200

if __name__ == "__main__":
    app.run(debug=True)
