import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Setup the Database & session
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Setup Flas
app = Flask(__name__)

# List all routes that are available 
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

# Convert the query results to a Dictionary using date as the key and prcp as the value.
    # Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation data"""
    # Query precipitation data
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of precipitation_data
    precipitation_data = []
    for precipitation in results:
        precipitation_dict = {}
        precipitation_dict["date"] = precipitation.date
        precipitation_dict["prcp"] = precipitation.prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)


# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():

    # Query all stations
    results = session.query(Station.name).all()

    return jsonify(results)


# Query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():

    # Query for the dates and temperature observations from a year from the last data point
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-22').order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of precipitation_data
    temp_data = []
    for temp in results:
        temp_dict = {}
        temp_dict["date"] = temp.date
        temp_dict["tobs"] = temp.tobs
        temp_data.append(temp_dict)

    return jsonify(temp_data)



if __name__ == '__main__':
    app.run(debug=True)