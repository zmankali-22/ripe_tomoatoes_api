from datetime import date


from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.movie import Movie
from models.actor import Actor

db_commands = Blueprint('db', __name__)


@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print('Tables Created successfully')


@db_commands.cli.command("seed")
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
    


@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped successfully")

