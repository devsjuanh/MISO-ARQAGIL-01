from flask import Flask
from flask_cors import CORS
from model import db
from vista import VistaSignIn
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config

def create_app(config_name):
    app = Flask(__name__)  
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['JWT_SECRET_KEY']='frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    return app

app = create_app('default')
app_context = app.app_context()
app_context.push()


db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaSignIn, '/')

jwt = JWTManager(app)
