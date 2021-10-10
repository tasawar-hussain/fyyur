#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import logging
import sys
from logging import FileHandler, Formatter
from datetime import datetime


from flask import (
    abort,
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
from flask_migrate import Migrate
from flask_moment import Moment
from sqlalchemy.orm import load_only

from forms import *
from models import db, Venue, Artist, Show
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
    venues = Venue.query.distinct(Venue.city, Venue.state).order_by(Venue.city).options(
        load_only(Venue.name, Venue.id, Venue.city, Venue.state)).all()

    result = {}
    for venue in venues:
        key = venue.city + ":" + venue.state
        num_upcoming_shows = Show.query.filter_by(venue_id=venue.id).filter(
            Show.start_time > datetime.now()).count()

        obj = {"id": venue.id, "name": venue.name,
               "num_upcoming_shows": num_upcoming_shows}
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
    query = request.form.get('search_term', '')
    result = Venue.query.filter(Venue.name.ilike(
        f"%{query}%")).options(load_only("name", "id")).all()

    response = {
        "count": len(result),
        "data": result
    }
    return render_template(
        'pages/search_venues.html',
        results=response, search_term=query
    )


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    data = Venue.query.get_or_404(venue_id)

    shows = Show.query.filter_by(venue_id=venue_id).join(Artist).all()
    current_time = datetime.now()
    past_shows = []
    upcoming_shows = []
    for show in shows:
        artist = show.artist
        show_data = {
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "artist_id": show.artist_id,
            "start_time": format_datetime(str(show.start_time))
        }
        if show.start_time > current_time:
            upcoming_shows.append(show_data)
        else:
            past_shows.append(show_data)

    venue = vars(data)

    venue["past_shows_count"] = len(past_shows)
    venue["upcoming_shows_count"] = len(upcoming_shows)
    venue["past_shows"] = past_shows
    venue["upcoming_shows"] = upcoming_shows

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
            flash("Form validation failed. Venue could not be created")
            return render_template('forms/new_venue.html', form=form)
    except:
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
        venue = Venue.query.get_or_404(venue_id)
        shows_count = Show.query.filter_by(venue_id=venue_id).count()

        if (shows_count > 1):
            flash(
                f"Venue ({venue.name}) can't be deleted, {shows_count} shows linked"
            )
            return redirect(url_for('show_venue', venue_id=venue_id))
        db.session.delete(venue)
        db.session.commit()
        flash(f"Venue ({venue.name}) deleted successfully ")
    except Exception as ex:
        print(str(ex))
        db.session.rollback()
        flash(f"Venue ({venue.name}) deletion failed")
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
        venue = Venue.query.get_or_404(venue_id)
        form = VenueForm(obj=venue)
        return render_template('forms/edit_venue.html', form=form, venue=venue)
    except:
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
    except:
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
    result = Artist.query.filter(Artist.name.ilike(f"%{query}%")).options(
        load_only("name", "id")).all()

    response = {"count": len(result), "data": result}

    return render_template('pages/search_artists.html',
                           results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id

    data = Artist.query.get_or_404(artist_id)

    shows = Show.query.filter_by(artist_id=artist_id).join(Venue).all()
    current_time = datetime.now()
    past_shows = []
    upcoming_shows = []
    for show in shows:
        venue = show.venue
        show_data = {
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": format_datetime(str(show.start_time))
        }
        if show.start_time > current_time:
            upcoming_shows.append(show_data)
        else:
            past_shows.append(show_data)

    artist = vars(data)
    artist["past_shows_count"] = len(past_shows)
    artist["upcoming_shows_count"] = len(upcoming_shows)
    artist["past_shows"] = past_shows
    artist["upcoming_shows"] = upcoming_shows
    return render_template('pages/show_artist.html', artist=artist)


#  Update Artist
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    try:
        artist = Artist.query.get_or_404(artist_id)

        form = ArtistForm(obj=artist)
        return render_template('forms/edit_artist.html',
                               form=form,
                               artist=artist)
    except:
        flash(f"Artist ({artist.id}) failed to fetch")

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
    except:
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
    except:
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
    data = []

    results = db.session.query(Show, Venue, Artist) \
        .join(Venue, Show.venue_id == Venue.id) \
        .join(Artist, Show.artist_id == Artist.id) \
        .order_by(Show.start_time.desc()) \
        .all()

    for show, venue, artist in results:  # 3 objects here!
        data.append({
            "venue_id": venue.id,
            "venue_name": venue.name,
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        })

    return render_template('pages/shows.html', shows=data)


#  Create Show
#  ----------------------------------------------------------------


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    venues = Venue.query.all()
    artists = Artist.query.all()
    form = ShowForm(venues=venues, artists=artists)
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    venues = Venue.query.all()
    artists = Artist.query.all()
    form = ShowForm(request.form, venues=venues, artists=artists)

    try:
        if form.validate():
            form_data = form.data
            del form_data['csrf_token']
            show = Show(**form_data)
            db.session.add(show)
            db.session.commit()
            flash("Show was successfully created!")
        else:
            print("errors: ", form.errors)
            flash("Form validation failed  Show could not be created")
            return render_template('forms/new_show.html', form=form)
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Venue could not be created.')
        return render_template('forms/new_show.html', form=form)
    finally:
        db.session.close()

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
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
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
