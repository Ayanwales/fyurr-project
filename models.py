from sqlalchemy import Column, String, Integer, Boolean, ARRAY, DateTime, create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Venue(db.Model):
  __tablename__ = 'Venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  
  genres = db.Column(db.ARRAY(db.String),nullable=False)
  website = db.Column(db.String(120))
  seeking_talent = db.Column(Boolean, default=False)
  seeking_description = db.column(String())
  #past_shows = db.Column(db.ARRAY(db.String))
  #upcoming_shows = db.Column(db.ARRAY(db.String))
  #past_shows_count = db.Column(db.Integer)
  #upcoming_shows_count = db.Column(db.Integer)
  shows = db.relationship('Show', backref='Venue',lazy=True)  
  def __repr__(self): 
   return f'<Venue ID: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, address: {self.address}, phone: {self.phone}, image_link: {self.image_link}, facebook_link: {self.facebook_link}, genres:{self.genres}, website:{self.website},seeking_talent: {self.seeking_talent},seeking_description:{self.seeking_description},past_shows:{self.past_shows},upcoming_shows: {self.upcoming_shows}, past_shows_count:{self.past_shows_count},upcoming_shows_count:{self.upcoming_shows_count}>'
    
class Artist(db.Model):
  __tablename__ = 'Artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  
  seeking_venue = db.Column(Boolean, default=False)
  seeking_description = db.Column(db.String())
  website =  db.Column(db.String(120))
  #past_shows = db.Column(db.ARRAY(db.String))
  #upcoming_shows = db.Column(db.ARRAY(db.String))
  #past_shows_count = db.Column(db.Integer)
  #upcoming_shows_count = db.Column(db.Integer)
  shows = db.relationship('Show', backref='Artist',lazy=True)
  def __repr__(self):
    return f'<Venue ID: {self.id},name: {self.name},city:{self.city},state:{self.state},genres:{self.genres},phone:{self.phone},image_link:{self.image_link},facebook_link:{self.facebook_link}, website:{self.website},past_shows:{self.past_shows},upcoming_shows:{self.upcoming_shows},seeking_venue:{self.seeking_venue},seeking_description:{self.seeking_description},past_shows_count:{self.past_shows_count},upcoming_shows_count:{self.upcoming_shows_count}>'

class Show (db.Model):
  __tablename__ = 'Show'
  id =  db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
    return f'<Show ID:{self.id}, artist_id: {self.artist_id},venue_id:{self.venue_id}, start_time:{self.start_time}>'
