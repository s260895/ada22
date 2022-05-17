from flask import Flask, request, jsonify
from database import db
from bson import ObjectId


app = Flask(__name__)


@app.route("/stocks", methods=["POST"])
def create_stock():
    """Endpoint to create stocks"""
    data = request.get_json()
    # return status 400 if request contains no body
    if not data:
        return "Request body is empty", 400
    # define the necessary data
    required_attrs = ["stock_id", "name", "prices", "ticker"]
    # check for necessary data, return status 400 is data is not available
    for required_attr in required_attrs:
        if required_attr not in data:
            return f"Missing required parameter `{required_attr}`.", 400
    # create object
    data_object = {attr: data[attr] for attr in required_attrs}
    db.stocks.insert_one(data_object)
    data_object["_id"] = str(data_object["_id"])
    return data_object, 201


@app.route("/stocks", methods=["GET"])
def get_stocks():
    """Endpoint to retrieve all stocks"""
    # get all stocks
    stocks = db.stocks.find()
    # return dict with all stocks
    return_list = []
    # convert the ObjectId and append to return_list
    for stock in stocks:
        stock["_id"] = str(stock["_id"])
        return_list.append(stock)
    return jsonify(return_list), 200


@app.route("/stocks/<stock_id>", methods=["PUT"])
def update_stock(stock_id):
    """Endpoint to update the price of a stock"""
    data = request.get_json()
    # return status 400 is necessary data is not available
    if "prices" not in data:
        return "Missing required parameter `prices`", 400
    # try to find the object, return status 400 is object_id is not correct
    try:
        stock = db.stocks.find_one({"_id": ObjectId(stock_id)})
    except Exception:
        return "Stock not found", 404

    # update object
    db.stocks.update_one({"_id": ObjectId(stock_id)}, {
        "$set": {
            "prices": data["prices"]
        }
    })
    return "Stock updated!", 202
