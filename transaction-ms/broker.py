import os
from google.cloud import pubsub_v1
from random import randint

# initialize google pub/sub
publisher = pubsub_v1.PublisherClient()


def create_transaction(transaction_type, stock_id, user_id):
    """Fuction to forward the transaction to the broker"""
    # create dummy data
    price = randint(0, 10)
    data = "New Transaction".encode("utf-8")
    # publish the message and print to console
    message = publisher.publish(
        os.environ["GOOGLE_TOPIC_PATH"],
        data,
        transaction_type=transaction_type,
        stock_id=str(stock_id),
        user_id=str(user_id),
        price=str(price))
    print("Transaction forwarded: {}".format(message.result()))
    # return the transaction data
    return {
        "transaction_type": transaction_type,
        "stock_id": stock_id,
        "user_id": user_id,
        "price": price,
    }
