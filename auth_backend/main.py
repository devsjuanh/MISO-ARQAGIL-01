from flask import Flask,jsonify
from flask_cors import CORS
from model import db
from vista import VistaSignIn
from flask_jwt_extended import JWTManager

from flask_restful import Api

app = Flask(__name__)

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaSignIn, '/signin')

jwt = JWTManager(app)