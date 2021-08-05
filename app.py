#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import logging
import sys
from logging import FileHandler, Formatter

from flask import (abort, Flask, Response, flash, redirect, render_template, request,
                   url_for)
from flask_migrate import Migrate
from flask_moment import Moment
from sqlalchemy.orm import load_only

from forms import *
from models import db, Venue, Artist
from filters import format_datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)

db.init_app(app)
migrate = Migrate(app, db, compare_type=True)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues = Venue.query.order_by("city").options(
        load_only("name", "id", "city", "state")).all()

    result = {}
    for venue in venues:
        key = venue.city + ":" + venue.state
        # TODO: implement upcoming shows count.
        obj = {"id": venue.id, "name": venue.name, "num_upcoming_shows": 3}
        if key in result:
            result[key]["venues"].append(obj)
        else:
            result[key] = {
                "city": venue.city,
                "state": venue.state,
                "venues": [obj]
            }
    data = result.values()
    return render_template('pages/venues.html', areas=data)

#  Search Venue
#  ----------------------------------------------------------------


@app.route('/venues/search', methods=['POST'])
def search_venues():
    """
    implement case-insensitive search on venues with partial string search.
    """
    query = request.form['search_term']
    result = Venue.query.filter(Venue.name.ilike(
        f"%{query}%")).options(load_only("name", "id")).all()

    response = {
        "count": len(result),
        "data": result
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # TODO: Add extra stats: past_shows, upcoming_shows,past_shows_count, upcoming_shows_count

    data = Venue.query.filter_by(id=venue_id).first()
    if not data:
        abort(404)

    venue = data.__dict__
    venue["past_shows_count"] = 1
    venue["upcoming_shows_count"] = 1
    venue["past_shows"] = []
    venue["upcoming_shows"] = []

    return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)
    try:
        if form.validate():
            form_data = form.data
            del form_data['csrf_token']
            venue = Venue(**form_data)
            db.session.add(venue)
            db.session.commit()
            flash("Venue was successfully created!")
        else:
            print("errors: ", form.errors)
            flash("Form validation failed .Venue could not be created")
            return render_template('forms/new_venue.html', form=form)
    except():
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Venue could not be created.')
        return render_template('forms/new_venue.html', form=form)
    finally:
        db.session.close()
    return redirect(url_for('venues'))


@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
    try:
        venue = Venue.query.filter_by(id=venue_id).first()
        if not venue:
            abort(404)
        db.session.delete(venue)
        db.session.commit()
        flash(f"Venue ({venue.name}) deleted successfully ")
    except():
        db.session.rollback()
        flash(f"Venue ({venue.name}) deletion failed ")
    finally:
        db.session.close()

    # BONUS CHALLENGE (Done): Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return redirect(url_for('index'))


#  Edit Venue
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    try:
        venue = Venue.query.filter_by(id=venue_id).first()
        if not venue:
            abort(404)
        form = VenueForm(obj=venue)
        return render_template('forms/edit_venue.html', form=form, venue=venue)
    except():
        flash(f"Venue ({venue.id}) failed to fetch")
    return None


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm(request.form)
    try:
        if form.validate():
            form_data = form.data
            del form_data['csrf_token']
            venue = db.session.query(Venue).filter_by(id=venue_id)

            if not venue.first():
                abort(404)
            venue.update(form_data)

            db.session.commit()
            flash("Venue successfully updated!")
        else:
            print("errors: ", form.errors)
            flash("Form validation failed .Venue could not be updated")
            return render_template('forms/new_venue.html', form=form)
    except():
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Venue could not be updated.')
        return render_template('forms/new_venue.html', form=form)
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    artists = Artist.query.options(load_only("name", "id")).all()

    return render_template('pages/artists.html', artists=artists)


#  Search Artist
#  ----------------------------------------------------------------

@app.route('/artists/search', methods=['POST'])
def search_artists():
    """
    implement case-insensitive search on artists with partial string search.
    """
    query = request.form['search_term']
    result = Artist.query.filter(Artist.name.ilike(
        f"%{query}%")).options(load_only("name", "id")).all()

    response = {
        "count": len(result),
        "data": result
    }

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id

    data = Artist.query.filter_by(id=artist_id).first()
    if not data:
        abort(404)

    artist = data.__dict__
    artist["past_shows_count"] = 3
    artist["upcoming_shows_count"] = 5
    artist["past_shows"] = []
    artist["upcoming_shows"] = []
    return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    try:
        artist = Artist.query.filter_by(id=artist_id).first()
        if not artist:
            abort(404)
        form = ArtistForm(obj=artist)
        return render_template('forms/edit_artist.html', form=form, artist=artist)
    except():
        flash(f"Artist ({artist.id}) failed to fetch")
    return None

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)
    try:
        if form.validate():
            form_data = form.data
            del form_data['csrf_token']
            artist = db.session.query(Artist).filter_by(id=artist_id)

            if not artist.first():
                abort(404)
            artist.update(form_data)

            db.session.commit()
            flash("Artist successfully updated!")
        else:
            print("errors: ", form.errors)
            flash("Form validation failed .Artist could not be updated")
            return render_template('forms/new_artist.html', form=form)
    except():
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. artist could not be updated.')
        return render_template('forms/new_artist.html', form=form)
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form)
    try:
        if form.validate():
            form_data = form.data
            del form_data['csrf_token']
            venue = Artist(**form_data)
            db.session.add(venue)
            db.session.commit()
            flash("Artist was successfully created!")
        else:
            print("errors: ", form.errors)
            flash("Form validation failed. Artist could not be created")
            return render_template('forms/new_artist.html', form=form)
    except():
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Artist could not be created.')
        return render_template('forms/new_artist.html', form=form)
    finally:
        db.session.close()
    return redirect(url_for('artists'))

#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = [
        {
            "venue_id": 1,
            "venue_name": "The Musical Hop",
            "artist_id": 4,
            "artist_name": "Guns N Petals",
            "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
            "start_time": "2019-05-21T21:30:00.000Z"
        }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 5,
            "artist_name": "Matt Quevedo",
            "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
            "start_time": "2019-06-15T23:00:00.000Z"
        }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-01T20:00:00.000Z"
        }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-08T20:00:00.000Z"
        }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-15T20:00:00.000Z"
        }]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
