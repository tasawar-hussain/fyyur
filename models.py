from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    genres = db.Column("genres", db.ARRAY(db.String()), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(
        500), default="https://cdn.pixabay.com/photo/2017/08/08/01/22/architecture-2610006_1280.jpg")
    facebook_link = db.Column(db.String(120), default="")
    website_link = db.Column(db.String(120), default="")
    seeking_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(120))

    def __repr__(self):
        return f'<Venue ID: {self.id}, name: {self.name}, city: {self.city}>'


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column("genres", db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(
        500), default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")
    facebook_link = db.Column(db.String(120), default="")
    website_link = db.Column(db.String(120), default="")
    seeking_venue = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(120))

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
