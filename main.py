import os
import random
import datetime
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Predefined Spend Categories and Transaction Types
SPEND_CATEGORIES = ["Essentials", "Transportation", "Lifestyle", "Debt Payments", "Savings and Investment"]
TRANSACTION_TYPES = ["Income", "Expense", "Saving"]

# Function to generate a single random transaction with realistic descriptions
def generate_random_transaction():
    # Generate random transaction data
    date = (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
    amount = round(random.uniform(50, 1000), 2)
    category = random.choice(SPEND_CATEGORIES)
    
    # Generate a more realistic description based on the category
    descriptions = {
        "Essentials": ["Bought groceries from SuperMart", "Paid monthly rent", "Paid electricity bill", "Bought household essentials"],
        "Transportation": ["Filled up fuel at Shell", "Paid for a taxi ride", "Bought a monthly bus pass", "Car maintenance service", "PRIMAX 95"],
        "Lifestyle": ["Gym membership fee", "Bought a new pair of running shoes", "Dinner at a fancy restaurant", "Streaming service subscription"],
        "Debt Payments": ["Paid credit card bill", "Mortgage payment", "Car loan installment", "Personal loan repayment"],
        "Savings and Investment": ["Transferred to savings account", "Invested in mutual funds", "Bought stocks", "Added to emergency fund"]
    }
    description = random.choice(descriptions[category])
    
    goal = None  # Set to None for now, but this can be filled in as needed
    transaction_type = random.choice(TRANSACTION_TYPES)

    # Create the transaction
    transaction = {
        "Amount": amount,
        "Category": category,
        "Date": date,
        "Description": description,
        "Goal": goal,
        "Type": transaction_type
    }

    return transaction

# Function to categorize a transaction based on description
def categorize_transaction(description):
    keywords = {
    "Essentials": ["groceries", "rent", "utilities", "food", "household"],
    "Transportation": ["taxi", "bus", "fuel", "transport", "car", "shell","primax"],
    "Lifestyle": ["shopping", "gym", "entertainment", "dinner", "subscription"],
    "Debt Payments": ["loan", "credit card", "mortgage", "installment"],
    "Savings and Investment": ["savings", "investment", "stocks", "fund"]
}
    
    
    for category, words in keywords.items():
        for word in words:
            if word in description.lower():
                return category
    return "Miscellaneous"

@app.route('/')
def home():
    return "API is working!"

@app.route('/affordability_check', methods=['POST'])
def affordability_check():
    print("affordability_check endpoint hit")
    # Parse JSON request data
    data = request.json
    purchase_amount = data.get('purchase_amount')
    available_budget = data.get('available_budget')
    monthly_savings_goal = data.get('monthly_savings_goal')
    category_spending = data.get('category_spending')

    # Calculate remaining budget for the selected category
    remaining_category_budget = available_budget - category_spending
    adjusted_budget = available_budget - purchase_amount

    # Affordability logic
    if purchase_amount <= remaining_category_budget:
        if adjusted_budget >= monthly_savings_goal:
            result = {
                "message": "Great job! You can afford this purchase and still meet your savings goal for this month.",
                "suggestion": "Consider setting aside any extra funds towards your long-term goals or an emergency fund."
            }
        else:
            result = {
                "message": "You can afford this purchase, but it will reduce your savings for this month.",
                "suggestion": "Be cautious with additional expenses to avoid impacting your future goals."
            }
        affordable = True
    else:
        result = {
            "message": "You cannot afford this purchase within your current budget.",
            "suggestion": "Consider postponing this purchase or reallocating funds from other categories."
        }
        affordable = False

    # Return JSON response
    return jsonify({
        "affordable": affordable,
        "result": result,
        "remaining_category_budget": remaining_category_budget,
        "adjusted_budget": adjusted_budget
    })

@app.route('/generate-transaction', methods=['GET'])
def generate_transaction():
    random_transaction = generate_random_transaction()
    return jsonify(random_transaction)

@app.route('/categorize-transaction', methods=['POST'])
def categorize():
    data = request.json
    description = data.get('description')
    category = categorize_transaction(description)
    return jsonify({"Category": category})

if __name__ == '__main__':
    # Use Render's port
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
