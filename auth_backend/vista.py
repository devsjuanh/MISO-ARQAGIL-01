from flask_restful import Resource
from flask import request
from model import db, User, UsuarioSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

usuario_schema = UsuarioSchema()

class VistaSignIn(Resource):

    def get(self):
        return {"mensaje":"hola mundo"}
    
    def post(self):
        nuevo_usuario = User(email=request.json["email"], password=request.json["password"])
        token_de_acceso = create_access_token(identity = request.json["email"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {"mensaje":"usuario creado exitosamente", "token de acceso":token_de_acceso}

    def put(self, id_usuario):
        usuario = User.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("password",usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = User.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '',204