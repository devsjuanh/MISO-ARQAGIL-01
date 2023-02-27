import os
from flask import Flask,jsonify
from flask_cors import CORS
import mysql.connector
import pika
import sys

## RabbitMQ connection
credentials = pika.PlainCredentials(username="guest", password="guest")
parameters = pika.ConnectionParameters("rabbitmq", credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='orders_queue', durable=True)

attemps = 0

def callback(ch, method, properties, body):
    global attemps

    attemps += 1
    if attemps % 10 == 0:
        print(" [x] Received %r" % body, file=sys.stderr)
        print(" [x] Attemps: %r" % attemps, file=sys.stderr)
        raise Exception("Error, attemps: %r" % attemps)

    print(" [x] Received %r" % body, file=sys.stderr)

channel.basic_consume(queue='orders_queue',
                      auto_ack=True,
                      on_message_callback=callback)

class DBManager:
    def __init__(self, database='example', host="db", user="root", password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user=user, 
            password=pf.read(),
            host=host, # name of the mysql service as set in the docker compose file
            database=database,
            auth_plugin='mysql_native_password'
        )
        pf.close()
        self.cursor = self.connection.cursor()
    
    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS inventory;')
        self.cursor.execute('CREATE TABLE inventory (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), cuantity INT);')
        self.cursor.executemany('INSERT INTO inventory (id, name, cuantity) VALUES (%s, %s, %s);', [(i, 'Product in inventory #%d'% i, i*100) for i in range (1,15)])

        self.cursor.execute('DROP TABLE IF EXISTS attemps;')
        self.cursor.execute('CREATE TABLE attemps (id INT AUTO_INCREMENT PRIMARY KEY);')
        self.connection.commit()
    
    def query_inventory(self):
        self.cursor.execute('SELECT name FROM inventory')
        rec = []
        for c in self.cursor:
            rec.append(c[0])
        return rec

## Server
server = Flask(__name__)
server.config['PROPAGATE_EXCEPTIONS'] = True
cors = CORS(server)

## DB connection
conn = DBManager(password_file='/run/secrets/db-password')
conn.populate_db()

@server.route('/start')
def startReadMQ():
    print("Server starting...")
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

@server.route('/inventory')
def listAllProductsInInventory():
    global conn

    try:
        rec = conn.query_inventory()
        resp = jsonify(rec)
        resp.status_code = 200
        return resp
    except Exception as exception:
        resp = jsonify(str(exception))
        resp.status_code = 500
        return resp


if __name__ == '__main__':
    print("Server starting...")
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    print("Server starting...")
    server.run()