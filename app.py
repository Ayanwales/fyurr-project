#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
# from sqlalchemy import Column, String, Integer, Boolean, ARRAY, DateTime, create_engine, ForeignKey
from flask_migrate import Migrate
from models import db, Venue, Artist, Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app,db)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2015@localhost:5432/dbfyurr'
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  # query the venue parameters
  venue_data = Venue.query.all()
  # creating empty json/dictionary
  venue_json = {}
  # looping through the data
  for venue_single in venue_data:
    key = f'{venue_single},{venue_single.state}'

    venue_json.setdefault(key,[]).append({
      "id": venue_single.id,
      "name": venue_single.name,
      "num_upcoming_shows" : len(venue_single.shows),
      "city": venue_single.city,
      "state": venue_single.state
    })
  
  data = []
  for value in venue_json.values():
    data.append({
      "city": value[0]['city'],
      "state": value[0]['state'],
      "venues": value
    })

  
      
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  
  search_items = Venue.query.filter(Venue.name.like('%' + request.form['search_term'] + '%')).all()
  
  response = {
    "count": len(search_items),
    "data": []
  }
  for search_item in search_items:  
    response["data"].append({
      "id" : search_item.id,
      "name": search_item.name,
      "num_upcoming_shows": search_item.upcoming_shows_count 
    })
  


  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  venue = Venue.query.get_or_404(venue_id)

  previous_shows = []
  next_shows = []
  show_values = None
  for show in venue.shows:
    show_values ={
      "artist_id": show.artist.id,
      "artist_name" : show.artist.image_link,
      "start_time" : show.start_time.strftime('%m/%d/%Y,%H:%M:%S')
    }
    if show.start_time <= datetime.now():
      previous_shows.append(show_values)
    else:
      next_shows.append(show_values)

  venue_item = {
    "id": venue.id,
    "name": venue.name,
    "genres":venue.genres,
    "address":venue.address,
    "city":venue.city,
    "state":venue.state,
    "phone":venue.phone,
    "website":venue.website,
    "facebook_link":venue.facebook_link,
    "seeking_talent":venue.seeking_talent,
    "seeking_description":venue.seeking_description,
    "image_link":venue.image_link,
    "past_shows":venue.previous_shows,
    "upcoming_shows":venue.next_shows,
    "past_shows_count":len(previous_shows),
    "upcoming_shows_count":len(upcoming_shows)
  }
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()
  try:
        new_venue_input = Venue(
            name = form.name.data,
            genres = form.genres.data,
            address = form.address.data,
            city = form.city.data,
            state = form.state.data,
            phone = form.phone.data,
            website = form.website.data,
            seeking_talent = form.seeking_talent.data,
            facebook_link = form.facebook_link.data,
            image_link = form.image_link.data
        )
        db.session.add(new_venue_input)
        db.session.commit()
      # TODO: insert form data as a new Venue record in the db, instead
      # TODO: modify data to be the data object returned from db insertion

      # on successful db insert, flash success
        flash('Venue ' + request.form ['name'] + ' was successfully listed!')
      # TODO: on unsuccessful db insert, flash an error instead.
  except:
        flash('An error occurred. Venue' + '' + request.form ['name'] + '' + 'could not be listed.')
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        db.session.rollback()
  finally:
        db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venue_deleted = Venue.query.get_or_404(venue_id)
  try:
    db.session.delete(venue_deleted)
    db.session.commit()
    flash('Venue' + venue_deleted + 'was successfully deleted!')
  except:
    db.session.rollback()
    flash('please try again. Venue' + venue_deleted + 'could not be deleted!')
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  
  # artists = db.session.query(Artist.id,Artist.name).all()
  artist_datas = Artist.query.all()
  data = []
  artist_json = {}
  for artist_data in artist_datas:
    artist_json = {
      "id": artist_data.id,
      "name" : artist_data.name
    }
    data.append(artist_json)
  return render_template('pages/artists.html', artist_datas=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_items = Artist.query.filter(Artist.name.like('%' + request.form['search_term'] + '%')).all()
  
  response = {
    "count": len(search_items),
    "data": []
  }
  for search_item in search_items:  
    response["data"].append({
      "id" : search_item.id,
      "name": search_item.name,
      "num_upcoming_shows": search_item.upcoming_shows_count 
    })
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get_or_404(artist_id)

  previous_shows = []
  next_shows = []
  show_values = None
  for show in artist.shows:
    show_values ={
      "venue_id": show.artist.id,
      "venue_name": show.venue.name,
      "venue_image" : show.artist.image_link,
      "start_time" : show.start_time.strftime('%m/%d/%Y,%H:%M:%S')
    }
    if show.start_time <= datetime.now():
      previous_shows.append(show_values)
    else:
      next_shows.append(show_values)

  artist_json = {
    "id": artist.id,
    "name": artist.name,
    "genres":artist.genres,
    "city":artist.city,
    "state":artist.state,
    "phone":artist.phone,
    "website":artist.website,
    "facebook_link":artist.facebook_link,
    "seeking_talent":artist.seeking_talent,
    "seeking_description":artist.seeking_description,
    "image_link":artist.image_link,
    "past_shows":artist.previous_shows,
    "upcoming_shows":artist.next_shows,
    "past_shows_count":len(previous_shows),
    "upcoming_shows_count":len(next_shows)
  }

  return render_template('pages/show_artist.html', artist=artist_json)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  if request.method == 'GET':
    artist = Artist.query.get(request.form.get(artist_id))
    artist.name = request.form['name']
    artist.genres = request.form['genres']
    artist.state = request.form['state']
    artist.city = request.form['city']
    artist.phone = request.form['phone']
    artist.seeking_venue = request.form['seeking_venue']
    artist.seeking_description = request.form['seeking_description']
    artist.facebook_link = request.form['facebook_link']
    artist.website = request.form['website']
    artist.image_link = request.form['image_link']
    db.session.commit()
  # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  if request.method == 'POST':
    artist = Artist.query.get(request.form.get(artist_id))
  try:
    artist.name = request.form['name']
    artist.genres = request.form['genres']
    artist.state = request.form['state']
    artist.city = request.form['city']
    artist.phone = request.form['phone']
    artist.seeking_venue = request.form['seeking_venue']
    artist.seeking_description = request.form['seeking_description']
    artist.facebook_link = request.form['facebook_link']
    artist.website = request.form['website']
    artist.image_link = request.form['image_link']
    db.session.commit()
    flash('Artist' + request.form['name'] +'was successfully updated')
  except:
    flash('An error occurred. artist ' + request.form['name'] + ' could not be updated.', category='error')
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  if request.method == 'GET':
    venue = Venue.query.get(request.form.get(venue_id))
    venue.name = request.form['name']
    venue.genres = request.form['genres']
    venue.state = request.form['state']
    venue.city = request.form['city']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.seeking_talent = request.form['seeking_talent']
    venue.seeking_description = request.form['seeking_description']
    venue.facebook_link = request.form['facebook_link']
    venue.website = request.form['website']
    venue.image_link = request.form['image_link']
    db.session.commit()
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  if request.method == 'POST':
    venue = Venue.query.get(request.form.get(venue_id))
  try:
    venue.name = request.form['name']
    venue.genres = request.form['genres']
    venue.state = request.form['state']
    venue.city = request.form['city']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.seeking_talent = request.form['seeking_talent']
    venue.seeking_description = request.form['seeking_description']
    venue.facebook_link = request.form['facebook_link']
    venue.website = request.form['website']
    venue.image_link = request.form['image_link']
    db.session.commit()
    flash('Venue' + request.form['name'] +'was successfully updated')
  except:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.', category='error')
    db.session.rollback()
  finally:
    db.session.close()
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    new_artist_input = Artist(
      name = form.name.Artist,
      genres = form.genres.Artist,
      city = form.city.Artist,
      state = form.state.Artist,
      phone = form.phone.Artist,
      website = form.website.Artist,
      seeking_venue = form.seeking_venue.Artist,
      facebook_link = form.facebook_link.Artist,
      image_link = form.image_link.Artist
    )
    db.session.add(new_artist_input)
    db.session.commit()
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  except:
    flash('An error occurred. Venue' + new_artist_input.name + 'could not be listed.')
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  finally:
    db.session.close()
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Show.query.all()
  data = []
  show_values = {}
  for show in shows:
    show_values = {
      "venue_id" : show.venue.id,
      "venue_name" : show.venue.name,
      "artist_id" : show.artist.id,
      "artist_name" : show.artist.name,
      "artist_image_link" : show.artist.image_link,
      "start_time" : show.start_time.strftime('%d/%m/Y,%H:%M:%S')
    }
    data.append(show_values)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    new_show = Show(
      artist_id = form.artist_id.data,
      venue_id = form.venue_id.data,
      start_time = form.start_time.data
    )
    db.session.add(new_show)
    db.session.commit()
   
  # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    flash('An error occurred. Show could not be listed.')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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
