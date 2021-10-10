from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateTimeField, SelectField,
                     SelectMultipleField, StringField)
from wtforms.validators import URL, DataRequired, Optional

from enums import Genre, State
from utils import is_valid_phone


class ShowForm(FlaskForm):
    def __init__(self, formdata=None, **kwargs):
        super().__init__(formdata, **kwargs)
        if 'venues' in kwargs:
            self.venue_id.choices = [(venue.id, venue.name)
                                     for venue in kwargs['venues']]
        if 'artists' in kwargs:
            self.artist_id.choices = [(artist.id, artist.name)
                                      for artist in kwargs['artists']]

    artist_id = SelectField('artist_id', validators=[DataRequired()])
    venue_id = SelectField('venue_id', validators=[DataRequired()])

    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=State.choices()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genre.choices()
    )
    image_link = StringField('image_link', validators=[Optional(), URL()])
    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL()])
    website_link = StringField('website_link', validators=[Optional(), URL()])
    seeking_talent = BooleanField('seeking_talent')
    seeking_description = StringField('seeking_description')

    def validate(self):
        """custom validate method in your Form:"""
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if self.phone.data and not is_valid_phone(self.phone.data):
            self.phone.errors.append('Invalid phone.')
            return False
        if not set(self.genres.data).issubset(dict(Genre.choices()).keys()):
            self.genres.errors.append('Invalid genres.')
            return False
        if self.state.data not in dict(State.choices()).keys():
            self.state.errors.append('Invalid state.')
            return False
        # if pass validation
        return True



class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=State.choices()
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField('image_link', validators=[Optional(), URL()])
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genre.choices()
    )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL()])
    website_link = StringField('website_link', validators=[Optional(), URL()])
    seeking_venue = BooleanField('seeking_venue')
    seeking_description = StringField('seeking_description')

    def validate(self):
        """custom validate method in your Form:"""
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if self.phone.data and not is_valid_phone(self.phone.data):
            self.phone.errors.append('Invalid phone.')
            return False
        if not set(self.genres.data).issubset(dict(Genre.choices()).keys()):
            self.genres.errors.append('Invalid genres.')
            return False
        if self.state.data not in dict(State.choices()).keys():
            self.state.errors.append('Invalid state.')
            return False
        # if pass validation
        return True
