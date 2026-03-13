from flask import Flask, request, jsonify
from db import insert_expenses,get_all_expenses,init_db

app=Flask(__name__)

@app.route("/expenses",methods=["POST"])
def create_expense():
    data = request.get_json()

    if not data:
        return jsonify({"error" : "Invalid JSON"}),400
    
    amount = data.get("amount")
    description = data.get("description")
    
    success,result = insert_expenses(amount,description)

    if not success:
        return jsonify({"error": result}) ,400
        
    return jsonify({"message":"Expense created","id":result}),201

@app.route("/expenses",methods=["GET"])
def get_expenses():
    success, result = get_all_expenses()

    

    if not success:
         return jsonify({"error": result}),500
        
    return jsonify(result),200

from db import delete_expense
@app.route("/expenses/<int:expense_id>",methods=["DELETE"])
def delete_expense_route(expense_id):
    status,error= delete_expense(expense_id)
   
    if status=="DELETED":
        return jsonify({"message":"Deleted successfully"}),200
    elif status=="NOT_FOUND":
        return jsonify({"error": "Expense not found"}),404
    else:
        return jsonify({"error":error}),500
from db import update_expense
@app.route("/expenses/<int:expense_id>" ,methods=["PUT"])
def update_expense_route(expense_id):
    data = request.get_json()
    if not data:
        return jsonify({"error":"Invalid JSON"}),400
    amount=data.get("amount")
    description=data.get("description")
    if amount is None or description is None:
        return jsonify({"error":"amount and description is required"}),400
    if not isinstance(amount, (int,float)):
        return jsonify({"error":"amount must be numeric"}), 400
    if amount<0:
        return jsonify({"error" : "amount can not be negative"}),400
    if not isinstance(description,str):
        return jsonify({"error":"description must be string"}),400
    if description.strip() =="":
        return jsonify({"error":"description can not be empty"}),400
    status, error = update_expense(expense_id, amount, description)
    if status == "UPDATED":
            return jsonify({"message": "Expense updated successfully"}), 200
    elif status =="NOT_FOUND":
            return jsonify({"error":"Expense not found"}), 404
    else:
        return jsonify({"error":error}),500
if __name__=="__main__":
    init_db()
    app.run(debug=True)
