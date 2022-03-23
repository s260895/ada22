from datetime import datetime
from flask import Flask, json, jsonify, request
from daos.stock_dao import StockDAO
from db import Session


class Stock:
  
    @staticmethod
    def create(body):
        session = Session()
        stock = StockDAO(body['name'], body['price'], body['ticker'])
        session.add(stock)
        session.commit()
        session.refresh(stock)
        session.close()
        return jsonify({'stock_id': stock.id}), 200

    @staticmethod
    def get():
        session = Session()
        stock = session.query(StockDAO)
        if stock:
           stock =
           session.close()
           return #what do i put here?
        else:
            session.close()
            return jsonify({'message': f'Database not found'}), 404
      
    @staticmethod
    def put(stock_id):
        session = Session()
        stock = session.query(StockDAO).filter(StockDAO.id == stock_id).first()

        if stock:
            text_out = {
                "name:": stock.name,
                "price": stock.price,
                "ticker": stock.ticker,
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no stock with id {stock_id}'}), 404