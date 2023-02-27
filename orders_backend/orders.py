#!/usr/bin/env python
from flask import Flask,jsonify
import json
from flask_cors import CORS
import pika
import os

params = pika.URLParameters('amqp://guest:guest@rabbitmq:5672/')
params.socket_timeout = 5

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='orders_queue', durable=True)

server = Flask(__name__)
server.config['PROPAGATE_EXCEPTIONS'] = True
cors = CORS(server)

@server.route('/orders', methods=['Post'])
def createOrder():
    global channel
    try:
        order = json.dumps(getMockOrder())
        channel.basic_publish(
                exchange='',
                routing_key='orders_queue', 
                body=order,
                properties=pika.BasicProperties(content_type='application/json')
            )
        resp = jsonify(getMockOrder())
        resp.status_code = 200
        print("[x] Sent 'Order to orders_queue'")
        return resp
    except Exception as exception:
        print("[Error] No send 'Order to orders_queue'")
        resp = jsonify(str(exception))
        resp.status_code = 500
        return resp

def getMockOrder():
    return {
        "id": 1,
        "customer": {
            "id": 1,
            "name": "John Doe",
            "email": "myemain@email.com",
        },
        "products": [
            {
                "id": 1,
                "name": "Product 1",
                "price": 10.0,
                "quantity": 1
            },
        ]
    }

if __name__ == '__main__':
    print("Server starting...")
    server.run()