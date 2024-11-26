from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/affordability_check', methods=['POST'])
def affordability_check():
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
            result = "You can afford this purchase and still meet your savings goal."
        else:
            result = "You can afford this purchase, but it will reduce your savings this month."
        affordable = True
    else:
        result = "You cannot afford this purchase within your budget."
        affordable = False

    # Return JSON response
    return jsonify({
        "affordable": affordable,
        "result": result,
        "remaining_category_budget": remaining_category_budget,
        "adjusted_budget": adjusted_budget
    })

if __name__ == '__main__':
    app.run(debug=True)
