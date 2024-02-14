from init import db,ma

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