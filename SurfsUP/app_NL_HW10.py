# Import the dependencies.
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
Base=automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
    """Start at the homepage."""
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Climate App Home Page<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"One Year of Precipitation Data:<br/>"
        f"/api/v1.0/precip<br/>"
        f"<br/>"
        f"List of Weather Stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature Observations from the Most Active Weather Station:<br/>" 
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Find the Minimum, Average and Maximum Temperatures for all Temperatures after a Specified Start Date (Format:yyy-mm-dd):<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"Find the Minimum, Average and Maximum Temperatures for Temperatures Between a Specified Start and End Date (Format:yyy-mm-dd/yyyy-mm-dd):<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precip")

def precipitation(): 

    # Create session (link) from Python to the DB
    session = Session(engine)

    """One Year of Precipitation Data"""
    # Perform a query to retrieve the data and precipitation scores
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    latest_date = dt.datetime.strptime(recent_date[0], '%Y-%m-%d')
    one_year_prior = dt.date(latest_date.year -1, latest_date.month, latest_date.day)
    sel = [measurement.date, measurement.prcp]
    date_prcp = session.query(*sel).filter(measurement.date >= one_year_prior).all()
    
    # Close session    
    session.close() 

    # Create a dictionary
    prcp_dict = []
    for date, prcp in date_prcp:
           prcp_step = {}
           prcp_step['date'] = date
           prcp_step['prcp'] = prcp
           prcp_dict.append(prcp_step)  

    # Return JSON response
    return jsonify(prcp_dict)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations") 

def all_stations():

    # Create session (link) from Python to the DB
    session = Session(engine)

    """List of All Stations in Dataset"""
    # Perform query to retrieve all stations in dataset
    results = session.query(station.name, station.station).all()

    # Close session    
    session.close() 

    # Convert the query results to a dictionary
    stations = []
    for station_name, station_id in results:
        station_data = {
            "station": station_id,
            "name": station_name
        }
        stations.append(station_data)

    # Return JSON response
    return jsonify(stations)

# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")  

def tobs():

    # Create session (link) from Python to the DB
    session = Session(engine)

    """One Year of Temperature Observations from the Most Active Station"""
    # Perform query to retrieve dates and temperatures of the most-active station for the previous year
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    latest_date = dt.datetime.strptime(recent_date[0], '%Y-%m-%d')
    one_year_prior = dt.date(latest_date.year -1, latest_date.month, latest_date.day)
    sel = [measurement.date, measurement.tobs]
    temps = session.query(*sel).filter(func.strftime(measurement.date) >= one_year_prior, measurement.station == 'USC00519281').\
        group_by(measurement.date).order_by(measurement.date).all()
    
    # Close session 
    session.close() 

    # Create a dictionary
    dict_tobs = []
    for date, temp in temps:
        tobs_step = {}
        tobs_step['date'] = date
        tobs_step['temp'] = temp
        dict_tobs.append(tobs_step)
        
    # Return JSON response
    return jsonify(dict_tobs)

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
@app.route("/api/v1.0/<start>") 

def start(start):

    # Create session (link) from Python to the DB
    session = Session(engine)

    # Perform query to retrieve min, avg, max temps from a specified start date to end of data
    query_start = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()

    # Close session 
    session.close() 

    # Create a dictionary
    start_date = []
    for min, avg, max in query_start:
        start_step = {}
        start_step["Minimum Temperature"] = min
        start_step["Average Temperature"] = avg
        start_step["Maximum Temperature"] = max
        start_date.append(start_step)

    # Return JSON response
    return jsonify(start_date)


# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range.
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>/<end>") 

def start_end(start, end):

    # Create session (link) from Python to the DB
    session = Session(engine)    

    # Perform query to retrieve min, avg, max temps from a specified start date and end date
    query_startend = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()

    # Close session 
    session.close() 

    # Create a dictionary
    start_end = []
    for min, avg, max in query_startend:
        start_end_step = {}
        start_end_step["Minimum Temperature"] = min
        start_end_step["Average Temperature"] = avg
        start_end_step["Maximum Temperature"] = max
        start_end.append(start_end_step)

    # Return JSON response
    return jsonify(start_end)

# Need this to close out everything
if __name__ == '__main__':
    app.run()