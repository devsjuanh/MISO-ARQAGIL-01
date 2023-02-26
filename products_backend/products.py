import os
from flask import Flask,jsonify
from flask_cors import CORS
import mysql.connector


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
        self.cursor.execute('DROP TABLE IF EXISTS products;')
        self.cursor.execute('CREATE TABLE products (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price INT);')
        self.cursor.executemany('INSERT INTO products (id, name, price) VALUES (%s, %s, %s);', [(i, 'Product #%d'% i, i*100) for i in range (1,15)])

        self.cursor.execute('DROP TABLE IF EXISTS attemps;')
        self.cursor.execute('CREATE TABLE attemps (id INT AUTO_INCREMENT PRIMARY KEY);')
        self.connection.commit()
    
    def query_products(self):
        self.cursor.execute('SELECT name FROM products')
        rec = []
        for c in self.cursor:
            rec.append(c[0])
        return rec


server = Flask(__name__)
server.config['PROPAGATE_EXCEPTIONS'] = True
cors = CORS(server)

conn = DBManager(password_file='/run/secrets/db-password')
conn.populate_db()

@server.route('/products')
def listAllProducts():
    global conn

    try:
        rec = conn.query_products()
        resp = jsonify(rec)
        resp.status_code = 200
        return resp
    except Exception as exception:
        resp = jsonify(str(exception))
        resp.status_code = 500
        return resp


if __name__ == '__main__':
    print("Server starting...")
    server.run()