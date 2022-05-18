from flask import Flask, request, jsonify
from database import db
from bson import ObjectId


app = Flask(__name__)


@app.route("/user_stocks", methods=["POST"])
def create_user_stock():
    """Endpoint to create user_stock"""
    body_data = request.get_json()
    # return status 400 if request contains no body
    if not body_data:
        return "No body", 400
    # define the necessary data
    required_data_list = ["stock_id", "user_id", "date_opened", "date_closed", "open_price", "close_price"]
    # check for necessary data, return status 400 is data is not available
    for required_data in required_data_list:
        if required_data not in body_data.keys():
            return "No {} in body".format(required_data), 400
    # create object
    data_object = {data_name:body_data[data_name] for data_name in required_data_list}
    db.userstocks.insert_one(data_object)
    data_object["_id"] = str(data_object["_id"])
    return data_object, 201


@app.route("/user_stocks", methods=["GET"])
def get_all_user_stocks():
    '''
    Endpoint to retrieve all user stocks
    '''
    # get all user_stocks
    objects = db.userstocks.find()
    # return dict with all userstocks in a strange way
    return_list = []
    # convert the ObjectId and append to return_list
    for object in objects:
        object["_id"] = str(object["_id"])
        return_list.append(object)
    return jsonify(return_list), 200


@app.route("/get-users/<stock_id>", methods=["GET"])
def get_users(stock_id):
    '''
    Endpoint to retrieve all users that have a certain stock
    '''
    # get all user_stocks
    objects = db.userstocks.find({"stock_id": stock_id})
    # return dict with all userstocks in a strange way
    return_list = []
    # append all user_ids to return_list
    for object in objects:
        return_list.append(object["user_id"])
    return jsonify(return_list), 200


@app.route("/user_stocks/<user_id>", methods=["PUT"])
def update_user_stock(user_id):
    request_data = request.get_json()
    # return status 400 is necessary data is not available
    if "close_price" not in request_data:
        return "No close_price", 400
    if "date_closed" not in request_data:
        return "No date_closed", 400
    # try to find the object, return status 400 is object_id is not correct
    try:
        db.userstocks.find_one({"user_id": ObjectId(user_id), "date_closed": {"$ne": None}})
    except:
        return "No user_stock found", 400

    # update object
    db.userstocks.update_one({"user_id": ObjectId(user_id), "date_closed": {"$ne": None}}, {
        "$set": {
            "date_closed": request_data["date_closed"],
            "close_price": request_data["close_price"]
        }
    })
    return "UserStock Sold!", 202
