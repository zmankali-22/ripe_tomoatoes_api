

from datetime import date, timedelta
from flask import Flask, request

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
            
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://tomato:123456@localhost:5432/ripe_tomatoes"
app.config["JWT_SECRET_KEY"] = "secret"

db = SQLAlchemy(app)
ma= Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255))
    length = db.Column(db.Integer)
    release_year = db.Column(db.Integer, nullable = False)

class MovieSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'length', 'genre','release_year')

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String)
    country = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)

class ActorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'gender', 'country', 'date_of_birth')

actors_schema = ActorSchema(many=True)
actor_schema = ActorSchema()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin')

users_schema = UsersSchema(many=True, exclude=['password'])
user_schema = UsersSchema(exclude=['password'])

@app.cli.command("create")
def create_tables():
    db.create_all()
    print('Tables Created successfully')


@app.cli.command("seed")
def seed_tables():
    movies = [
         Movie(
             title="Movie 1",
             genre="Comedy",
             length=120,
             release_year=2019

         ),
         Movie(
             title="Movie 2",
             genre="Drama",
             length=130,
             release_year=2020
         )
         ]
    
    actors = [
        Actor(
            first_name="John",
            last_name="Doe",
            gender="Male",
            country="UK",
            date_of_birth=date(2000, 1, 1)
        ),
        Actor(
            first_name="Smitha",
            last_name="Patil",
            gender="Female",
            country="USA",
        ),
        Actor(
            first_name="Jane",
            last_name="Parker",
            gender="Female",
            country="Japan",
            date_of_birth=date(1998, 10, 1)
        ),
        Actor(  
            first_name="Kevin",
            last_name="Roland",
            gender="Male",
            country="Nepal",
            date_of_birth=date(1997, 8, 12)
        )
    ]

    users = [
        User(
            name = "John",
            email = "john@gmail.com",
            password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
            is_admin = True
        ),
        User(
            name = "Sujita",
            email = "sujita@gmail.com",
            password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
            is_admin = False
        )
    ]
    db
    db.session.add_all(movies)
    db.session.add_all(actors)
    db.session.add_all(users)
    db.session.commit()
    print("Tables seeded successfully")
    


@app.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped successfully")


@app.route("/")
def index():
    return "Welcome to Ripe Tomatoes API"
@app.route('/movies')
def get_movies():
    stmt = db.select(Movie)
    movies_list = db.session.scalars(stmt)
    data = movies_schema.dump(movies_list)
    return data

@app.route('/movies/<int:movie_id>')
def get_movie(movie_id):
    stmt = db.select(Movie).filter_by(id=movie_id)
    movie  = db.session.scalar(stmt)
    if movie:

        data = movie_schema.dump(movie)
        return data
    else:
        return {"error": f"Movie with {movie_id} not exist "}, 404
    
@app.route('/actors')
def get_actors():
    stmt = db.select(Actor)
    actors_list = db.session.scalars(stmt)
    data = actors_schema.dump(actors_list)
    return data

@app.route('/actors/<int:actor_id>')
def get_actor(actor_id):
    stmt = db.select(Actor).filter_by(id=actor_id)
    actor  = db.session.scalar(stmt)
    if actor:

        data = actor_schema.dump(actor)
        return data
    else:
        return {"error": f"Actor with {actor_id} not exist "}, 404
    
@app.route("/movies", methods=["POST"])
@jwt_required()
def create_movie():
    # return "post method "
    movie_fields = request.get_json()
    print(movie_fields)
    new_movie = Movie(
        title = movie_fields.get('title'),
        genre = movie_fields.get('genre'),
        length = movie_fields.get('length'),
        release_year = movie_fields.get('release_year')
    )
    db.session.add(new_movie)
    db.session.commit()
    data = movie_schema.dump(new_movie)
    return data, 201

@app.route("/actors", methods=["POST"])
@jwt_required()
def create_actor():
    # return "post method "
    actor_fields = request.get_json()
    print(actor_fields)
    new_actor = Actor(
       first_name=actor_fields.get('first_name'),
       last_name=actor_fields.get('last_name'),
       gender=actor_fields.get('gender'),
       country=actor_fields.get('country'),
       date_of_birth=actor_fields.get('date_of_birth')
    )
    db.session.add(new_actor)
    db.session.commit()
    data = actor_schema.dump(new_actor)
    return data, 201


@app.route("/movies/<int:movie_id>", methods = ["PUT", "PATCH"])
def update_movie(movie_id):
    stmt = db.select(Movie).where(Movie.id == movie_id)
    movie = db.session.scalar(stmt)
    movie_fields = request.get_json()
    if movie:
        movie.title = movie_fields.get("title") or movie.title
        movie.genre = movie_fields.get("genre") or movie.genre
        movie.length = movie_fields.get("length") or movie.length
        movie.release_year = movie_fields.get("release_year") or movie.release_year
        db.session.commit()
        data = movie_schema.dump(movie)
        return data
    else:
        return {"error": f"Movie with {movie_id} not exist "}, 404
    
@app.route("/actors/<int:actor_id>", methods = ["PUT", "PATCH"])
def update_actor(actor_id):
    stmt = db.select(Actor).where(Actor.id == actor_id)
    actor = db.session.scalar(stmt)
    actor_fields = request.get_json()
    if actor:
        actor.first_name = actor_fields.get('first_name') or actor.first_name
        actor.last_name = actor_fields.get('last_name') or actor.last_name
        actor.gender = actor_fields.get('gender') or actor.gender
        actor.country = actor_fields.get('country') or actor.country
        actor.date_of_birth = actor_fields.get('date_of_birth') or actor.date_of_birth

        db.session.commit()
        data = actor_schema.dump(actor)
        return data
    else:
        return {"error": f"Actor with {actor_id} not exist "}, 404

@app.route("/movies/<int:movie_id>", methods = ["DELETE"])
@jwt_required()
def delete_movie(movie_id):
    is_admin = authoriseAdmin()
    if not is_admin:
        return {"error": "You are not authorized to delete this movie"}, 403
    stmt = db.select(Movie).where(Movie.id == movie_id)
    movie = db.session.scalar(stmt)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return {"message": f"Movie  {movie.title} deleted"}
    else:
        return {"error": f"Movie with {movie_id} not exist "}, 404
    

@app.route("/actors/<int:actor_id>", methods = ["DELETE"])
@jwt_required()
def delete_actor(actor_id):
    is_admin = authoriseAdmin()
    if not is_admin:
        return {"error": "You are not authorized to delete this actor"}, 403
    stmt = db.select(Actor).where(Actor.id == actor_id)
    actor = db.session.scalar(stmt)
    if actor:
        db.session.delete(actor)
        db.session.commit()
        return {"message": f"Actor  {actor.first_name} {actor.last_name} deleted"}
    else:
        return {"error": f"Actor with {actor_id} not exist "}, 404
    

@app.route("/auth/signup", methods=["POST"])
def signup():
    try:
        user_fields = request.get_json()
        password = user_fields.get("password")
        hashed_password = bcrypt.generate_password_hash(password).decode("utf=8")
        user = User(
            name = user_fields.get("name"),
            email = user_fields.get("email"),
            password = hashed_password
           
        )
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201
    except IntegrityError:
        return {"error": f"Email address already exists in database"}, 409
    
@app.route("/auth/signin", methods=["POST"])
def login():
    user_fields = request.get_json()

    stmt = db.select(User).filter_by(email=user_fields.get("email"))
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, user_fields.get("password")):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {"email": user.email, "token": token, "is_admin": user.is_admin}
    else:
        return {"error": "Invalid credentials email or password"}, 401
    

def authoriseAdmin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin
