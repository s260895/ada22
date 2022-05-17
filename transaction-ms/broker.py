import os
import json
from google.cloud import pubsub_v1
from random import randint

# initialize google pub/sub
publisher = pubsub_v1.PublisherClient()


def create_transaction(transaction_type, stock_id, user_id):
    """Fuction to forward the transaction to the broker"""
    # create dummy data
    data = {
        "transaction_type": transaction_type,
        "stock_id": stock_id,
        "user_id": user_id,
        "price": randint(0, 10),
    }

    data = json.dumps(data).encode("utf-8")
    # publish the message and print to console
    message = publisher.publish(os.environ["GOOGLE_TOPIC_PATH"], data)
    print("Transaction forwarded: {}".format(message.result()))
    # return the transaction data
    return data
