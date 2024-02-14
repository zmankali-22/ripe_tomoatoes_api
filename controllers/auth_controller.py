from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from psycopg2 import errorcodes

from init import db, bcrypt
from models.user import User, user_schema

auth_bp = Blueprint('auth',__name__, url_prefix='/auth')


@auth_bp.route("/signup", methods=["POST"])
def signup():
    try:
        user_fields = request.get_json()
      
        user = User(
            name = user_fields.get("name"),
            email = user_fields.get("email"),
           
           
        )
        password = user_fields.get("password")
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} is required"}
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": f"The email address already exists"}, 409
    

@auth_bp.route("/auth/signin", methods=["POST"])
def login():
    user_fields = request.get_json()

    stmt = db.select(User).filter_by(email=user_fields.get("email"))
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, user_fields.get("password")):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {"email": user.email, "token": token, "is_admin": user.is_admin}
    else:
        return {"error": "Invalid credentials email or password"}, 401
    