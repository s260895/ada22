from datetime import datetime
from flask import Flask, json, jsonify, Response, request
from daos.stock_dao import StockDAO
from db import Session

app = Flask(__name__)

@app.route('/stocks', methods = ['POST'])
def create(body):
    session = Session()
    stock = StockDAO(body['name'], body['price'], body['ticker'])
    session.add(stock)
    session.commit()
    session.refresh(stock)
    session.close()
    return jsonify({'message': f'stock with id {stock.stock_id} created'}), 200

@app.route('/stocks', methods=['GET'])
def get():
        session = Session()
        stock = session.query(StockDAO).all()
        if stock:
           session.close()
           return json.dumps(stock), 200
           
        else:
            session.close() 
            return jsonify({'message': f'Database not found'}), 404

@app.route('/stocks/<stock_id>', methods=['PUT'])
def update(stock_id, body):
        session = Session()
        stock = session.query(StockDAO).filter(StockDAO.stock_id == stock_id).first()
        if stock:
            stock.name = body['name']
            stock.price = body['price']
            stock.ticker = body['ticker']
            session.close()
            return jsonify({'message:': f'Stock at id {stock_id} updated'}), 200
        else:
            session.close()
            return jsonify({'message': f'There is no stock with id {stock_id}'}), 404