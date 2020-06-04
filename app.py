import numpy as np
import pandas as pd
import datetime as dt


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitaion<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
    )

@app.route("/api/v1.0/precipitaion")
def precipitaion():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(measurement.date, measurement.prcp).filter(measurement.date >= query_date).all()
    prcp = {date: prcp for date, prcp in precipitation}
    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(station.station).all()
    #will use for all other queries (need to make a list to jsonify)
    stat = list(np.ravel(stations))
    return jsonify(stat)

@app.route("/api/v1.0/tobs")
def tobs():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    station_temp = session.query(measurement.tobs).filter(measurement.date >= query_date).filter(measurement.station == 'USC00519281').all()
    tob = list(np.ravel(station_temp))
    return jsonify(tob)

@app.route("/api/v1.0/temp/<start>")
def statsstart(start):
    results = session.query(func.max(measurement.tobs), func.min(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).all()
    starttobs = list(np.ravel(results))
    return jsonify(starttobs)

@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start, end):
    results = session.query(func.max(measurement.tobs), func.min(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date <= end).filter(measurement.date >= start).all()
    statstobs = list(np.ravel(results))
    return jsonify(statstobs)

if __name__ == '__main__':
    app.run(debug=True)

