# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

application = Flask(__name__)

#################################################
# Flask Routes
#################################################
# 1) "/"
#    Start at the homepage. 
#    List all the available routes.
#################################################

@application.route("/")
def welcome():
    session = Session(engine)

    """List all the available routes."""

    session.close()

    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of stations: /api/v1.0/stations<br/>"
        f"Temperature observations for one year: /api/v1.0/tobs<br/>"
        f"Temperature statistics from the start date (YYYY-MM-DD): /api/v1.0/<start><br/>"
        f"Temperature statistics from between two dates (YYYY-MM-DD): /api/v1.0/<start>/<end>"
    )

#################################################
# 2) "/api/v1.0/precipitation"
#    Convert the query results from your precipitation analysis to a dictionary using date as the key and prcp as the value.
#    Return the JSON representation of your dictionary.
#################################################

@application.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    start_date = '2016-08-23'
    selection = [Measurement.date, Measurement.prcp]

    # Query for the precipitation data within the last year
    results = session.query(*selection)\
            .filter(Measurement.date >= start_date)\
            .group_by(Measurement.date)\
            .order_by(Measurement.date).all()
    
    precipitation_data = {date: prcp for date, prcp in results}

    session.close()
    return jsonify(precipitation_data)

#################################################
# 3) "/api/v1.0/stations"
#    Return a JSON list of stations from the dataset.
#################################################

@application.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # Query for the list of stations
    results = session.query(Station.station).all()
    station_list = [station[0] for station in results]

    session.close()
    return jsonify(station_list)

#################################################
# 4) "/api/v1.0/tobs"
#    Query the dates and temperature observations of the most-active station for the previous year of data.
#    Return a JSON list of temperature observations for the previous year.
#################################################

@application.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    most_active_station = 'USC00519281'
    start_date= '2016-08-23'
    selection = [Measurement.date, Measurement.tobs]

    # Query for the temperature observations in the last year
    results = session.query(*selection)\
                    .filter(Measurement.date >= start_date)\
                    .filter(Measurement.station == most_active_station)\
                    .group_by(Measurement.date)\
                    .order_by(Measurement.date).all()

    tobs_list = [{"Date": date, "Temperature": tobs} for date, tobs in results]

    session.close()
    return jsonify(tobs_list)

#################################################
# 5) "/api/v1.0/<start>" AND "/api/v1.0/<start>/<end>"
#    Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#    For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
#    For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
#################################################



# Run the app
if __name__ == "__main__":
    application.run(debug=True)