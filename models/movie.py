from init import db,ma

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
