from flask import Flask,jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
db = SQLAlchemy(app)