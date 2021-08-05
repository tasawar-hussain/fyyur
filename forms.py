from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateTimeField, SelectField,
                     SelectMultipleField, StringField)
from wtforms.validators import URL, AnyOf, DataRequired, Optional

from choices import state_choices, genre_choices


class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id', validators=[DataRequired()]
    )
    venue_id = StringField(
        'venue_id', validators=[DataRequired()]
    )
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
        choices=state_choices
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=genre_choices
    )
    image_link = StringField('image_link', validators=[Optional(), URL()])
    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL()])
    website_link = StringField('website_link', validators=[Optional(), URL()])
    seeking_talent = BooleanField('seeking_talent')
    seeking_description = StringField('seeking_description')


class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=state_choices
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField('image_link', validators=[Optional(), URL()])
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=genre_choices
    )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL()])
    website_link = StringField('website_link', validators=[Optional(), URL()])
    seeking_venue = BooleanField('seeking_venue')
    seeking_description = StringField('seeking_description')
