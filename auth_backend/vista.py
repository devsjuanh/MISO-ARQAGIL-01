from flask_restful import Resource
from flask import request
from model import db, User, UsuarioSchema, Role
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from role import check_access

usuario_schema = UsuarioSchema()

class VistaSignIn(Resource):

    @check_access(roles=[Role.ADMIN, Role.VENDEDOR])
    def get(self):
        return {"mensaje":"hola mundo"}
    
    def post(self):
        user_role = None
        if request.json.get("role", None) is None:
            user_role = Role.VENDEDOR
        nuevo_usuario = User(
            email=request.json["email"], 
            password=request.json["password"], 
            role=user_role)
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