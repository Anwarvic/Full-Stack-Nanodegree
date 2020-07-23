#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from collections import defaultdict
from flask import Flask, render_template, request, Response, \
    flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(2))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(sqlalchemy.types.ARRAY(db.String))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue', lazy=True,
                cascade="all,delete")


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(sqlalchemy.types.ARRAY(db.String))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist', lazy=True,
            cascade="all,delete")


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id= db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime())


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

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
    # replace with real venues data.
    # num_shows should be aggregated based on number of shows per venue.
    try:
        venues = defaultdict(list)
        for venue in Venue.query.all():
            venues[(venue.city, venue.state)].append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows":
                    len([s.start_time > datetime.now() for s in venue.shows])
            })
        data = []
        for key, value in venues.items():
            data.append({
                "city": key[0],
                "state": key[1],
                "venues": value
            })
        return render_template('pages/venues.html', areas=data)
    except Exception as ex:
        print(ex)
        flash("An error occurred!!")
        return render_template('pages/home.html')


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # implement search on venues with partial string search.
    # Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    response = {
        "count": len(venues),
        "data": [{
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": 
                len([s for s in venue.shows if s.start_time > datetime.now()])
        } for venue in venues]
    }
    return render_template('pages/search_venues.html', results=response,
                            search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # replace with real venue data from the venues table, using venue_id
    try:
        venue = Venue.query.get(venue_id)
        if venue is None:
            raise ValueError(f"Venue whose id is {venue_id} can't be found!!")
        past_shows = [{
            "artist_id": s.artist_id,
            "artist_name": s.artist.name,
            "artist_image_link": s.artist.image_link,
            "start_time": str(s.start_time)
        } for s in venue.shows if s.start_time < datetime.now()]
        
        upcoming_shows = [{
            "artist_id": s.artist_id,
            "artist_name": s.artist.name,
            "artist_image_link": s.artist.image_link,
            "start_time": str(s.start_time)
        } for s in venue.shows if s.start_time >= datetime.now()]
        
        data = {
            "id": venue.id,
            "name": venue.name,
            "genres": venue.genres,
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website": venue.website,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description": venue.seeking_description,
            "image_link": venue.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows)
        }
        return render_template('pages/show_venue.html', venue=data)
    except Exception as ex:
        print(ex)
        flash('An error occurred!')
        return render_template('pages/home.html')


#  Create Venue
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET']) 
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # insert form data as a new Venue record in the db
    # on successful db insert, flash success
    # on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    myform = VenueForm()
    # check validation rules
    if not myform.validate():
        for key, value in myform.errors.items():
            if myform[key].data != '':
                flash(value[0])
        return render_template('forms/new_venue.html', form=myform)
    # extract needed information
    try:
        vn = Venue(
            name = myform.name.data,
            city = myform.city.data,
            state = myform.state.data,
            address = myform.address.data,
            phone = myform.phone.data,
            image_link = myform.image_link.data,
            genres = myform.genres.data,
            website = myform.website.data,
            facebook_link = myform.facebook_link.data,
            seeking_talent = myform.seeking_talent.data,
        )
        vn.seeking_description = myform.seeking_description.data \
            if myform.seeking_talent.data else ""
        db.session.add(vn)
        db.session.commit()
        flash(f'Venue `{myform.name.data}` was successfully created!')
    except Exception as ex:
        print(ex)
        db.session.rollback()
        flash(f'An error occurred. Venue `{myform.name.data}` could not be created!')
    finally:
        db.session.close()
    return render_template('pages/home.html')


#  Delete Venue
#  ----------------------------------------------------------------
@app.route('/venues/<venue_id>', methods=['DELETE', 'POST'])
def delete_venue(venue_id):
    # Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record.
    # Handle cases where the session commit could fail.
    try:
        vn = Venue.query.get(venue_id)
        if vn is None:
            raise ValueError(f"Venue whose id is: `{venue_id}` isn't found!!")
        db.session.delete(vn)
        db.session.commit()
        flash(f'Venue `{vn.name}` was successfully deleted!')
    except Exception as ex:
        print(ex)
        db.session.rollback()
        flash(f"Venue whose id is `{venue_id}` couldn't get deleted!")
    finally:
        db.session.close()
        return render_template('pages/home.html')


#  Update Venue
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):   
    # populate form with values from venue with ID <venue_id>
    try:
        venue = Venue.query.get(venue_id)
        if venue is None:
            raise ValueError(f"Venue whose id is {venue_id} can't be found!!")
        myform = VenueForm()
        myform.state.process_data(venue.state)
        myform.genres.process_data(venue.genres)
        return render_template('forms/edit_venue.html', form=myform,
                venue=venue)
    except Exception as ex:
        print(ex)
        flash("An error occurred!!")
        return render_template('pages/home.html')


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    myform = VenueForm()
    # check validation rules
    if not myform.validate():
        for key, value in myform.errors.items():
            if myform[key].data != '':
                flash(value[0])
        return redirect(url_for('show_venue', venue_id=venue_id))
    # update values
    try:
        vn = Venue.query.get(venue_id)
        if vn is None:
            raise ValueError(f"Venue whose id is {venue_id} can't be found!!")
        vn.name = myform.name.data
        vn.city = myform.city.data
        vn.state = myform.state.data
        vn.phone = myform.phone.data
        vn.image_link = myform.image_link.data
        vn.genres = myform.genres.data
        vn.website = myform.website.data
        vn.facebook_link = myform.facebook_link.data
        vn.seeking_talent = myform.seeking_talent.data
        vn.seeking_description = myform.seeking_description.data \
            if myform.seeking_talent.data else ""
        db.session.commit()
        flash(f'Venue `{vn.name}` was successfully edited!')
    except Exception as ex:
        print(ex)
        db.session.rollback()
        flash("An error occurred. Venue `{myform.name.data}` couldn't be edited!")
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))










#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # replace with real data returned from querying the database
    try:
        data = [{"id": artist.id, "name": artist.name} \
            for artist in Artist.query.all()]
        return render_template('pages/artists.html', artists=data)
    except Exception as ex:
        print(ex)
        flash("An error occurred!!")
        return render_template('pages/home.html')


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # implement search on artists with partial string search.
    # Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    response = {
        "count": len(artists),
        "data": [{
            "id":  artist.id,
            "name": artist.name,
            "num_upcoming_shows": 
                len([s for s in artist.shows if s.start_time > datetime.now()])
        } for artist in artists]
    }
    return render_template('pages/search_artists.html', results=response,
                            search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # replace with real venue data from the venues table, using venue_id
    try:
        artist = Artist.query.get(artist_id)
        if artist is None:
            raise ValueError(f"Artist whose id is {artist_id} can't be found!!")
        past_shows = [{
            "venue_id": s.venue_id,
            "venue_name": s.venue.name,
            "venue_image_link": s.venue.image_link,
            "start_time": str(s.start_time)
        } for s in artist.shows if s.start_time < datetime.now()]
        
        upcoming_shows = [{
            "venue_id": s.venue_id,
            "venue_name": s.venue.name,
            "venue_image_link": s.venue.image_link,
            "start_time": str(s.start_time)
        } for s in artist.shows if s.start_time >= datetime.now()]
        
        data = {
            "id": artist.id,
            "name": artist.name,
            "genres": artist.genres,
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "website": artist.website,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows)
        }
        return render_template('pages/show_artist.html', artist=data)
    except Exception as ex:
        print(ex)
        flash('An error occurred!')
        return render_template('pages/home.html')


#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # insert form data as a new Venue record in the db, instead
    # modify data to be the data object returned from db insertion
    # on successful db insert, flash success
    # on unsuccessful db insert, flash an error instead.
    myform = ArtistForm()
    # check validation rules
    if not myform.validate():
        for key, value in myform.errors.items():
            if myform[key].data != '':
                flash(value[0])
        return render_template('forms/new_artist.html', form=myform)
    try:
        artist = Artist(
            name = myform.name.data,
            city = myform.city.data,
            state = myform.state.data,
            phone = myform.phone.data,
            image_link = myform.image_link.data,
            genres = myform.genres.data,
            website = myform.website.data,
            facebook_link = myform.facebook_link.data,
            seeking_venue = myform.seeking_venue.data,
        )
        artist.seeking_description = myform.seeking_description.data \
            if artist.seeking_venue else ""
        db.session.add(artist)
        db.session.commit()
        flash(f'Artist `{myform.name.data}` was successfully created!')
    except Exception as ex:
        print(ex)
        db.session.rollback()
        flash(f'An error occurred. Artist `{myform.name.data}` could not be created.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Delete Artist
#  ----------------------------------------------------------------
@app.route('/artists/<artist_id>', methods=['DELETE', 'POST'])
def delete_artist(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        if artist is None:
            raise ValueError(f"Artist whose id is: `{artist_id}` isn't found!!")
        db.session.delete(artist)
        db.session.commit()
        flash(f'Artist `{artist.name}` was successfully deleted!')
    except Exception as ex:
        print(ex)
        db.session.rollback()
        flash(f"Artist whose id is `{artist_id}` couldn't get deleted!")
    finally:
        db.session.close()
        return render_template('pages/home.html')


#  Update Artist
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    # populate form with fields from artist with ID <artist_id>
    try:
        myform = ArtistForm()
        artist = Artist.query.get(artist_id)
        if artist is None:
            raise ValueError(f"Artist whose id is {artist_id} can't be found!!")
        myform.state.process_data(artist.state)
        myform.genres.process_data(artist.genres)
        return render_template('forms/edit_artist.html', form=myform,
                artist=artist)
    except Exception as ex:
        print(ex)
        flash("An error occurred!!")
        return render_template('pages/home.html')


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    myform = ArtistForm()
    # check validation rules
    if not myform.validate():
        for key, value in myform.errors.items():
            if myform[key].data != '':
                flash(value[0])
        return redirect(url_for('show_artist', artist_id=artist_id))
    # update values
    try:
        artist = Artist.query.get(artist_id)
        if artist is None:
            raise ValueError(f"Artist whose id is {artist_id} can't be found!!")
        artist.name = myform.name.data
        artist.city = myform.city.data
        artist.state = myform.state.data
        artist.phone = myform.phone.data
        artist.image_link = myform.image_link.data
        artist.genres = myform.genres.data
        artist.website = myform.website.data
        artist.facebook_link = myform.facebook_link.data
        artist.seeking_venue = myform.seeking_venue.data
        artist.seeking_description = myform.seeking_description.data \
            if myform.seeking_venue.data else ""
        db.session.commit()
        flash(f'Artist `{artist.name}` was successfully edited!')
    except Exception as ex:
        print(ex)
        db.session.rollback()
        flash(f"An error occurred. Artist `{myform.name.data}` couldn't be edited!")
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))








#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # replace with real venues data.
    try:
        data = [
            {
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "artist_id": show.artist_id,
                "artist_name": show.artist.name,
                "artist_image": show.artist.image_link,
                "start_time": str(show.start_time)
            }
            for show in Show.query.all()
        ]
        return render_template('pages/shows.html', shows=data)
    except Exception as ex:
        print(ex)
        flash("An error occurred!!")
        return render_template('pages/home.html')


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # insert form data as a new Show record in the db, instead
    # on successful db insert, flash success
    # flash('Show was successfully created!')
    # on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    myform = ShowForm()
    # check validation rules
    if not myform.validate():
        for key, value in myform.errors.items():
            if myform[key].data != '':
                flash(value[0])
        return render_template('forms/new_show.html', form=myform)
    try:
        show = Show(
            artist_id = myform.artist_id.data,
            venue_id = myform.venue_id.data,
            start_time = myform.start_time.data
        )
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully created!')
    except Exception as ex:
        print(ex)
        db.session.rollback()
        flash('An error occurred. Show could not be created!')
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
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
