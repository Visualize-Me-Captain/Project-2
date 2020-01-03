import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template
import os


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///data/hist_trips.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
# Trips = Base.classes.hist_trips
# Stations = Base.classes.stations

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# set up global variables to be used throughout the dashboard
#################################################

# Capture all data from the hist_trips table inside hist_trips.sqlite
riders_tbl = pd.read_sql("SELECT * FROM hist_trips", con=engine)

# Capture alld data from the stations table inside hist_trips.sqlite
stations_tbl = pd.read_sql("SELECT * FROM stations", con=engine)

# Join station name on from station id
from_station_name = pd.merge(riders_tbl, stations_tbl, left_on='from_station_id', right_on='ID')

 # Peform another join to also add station name for the to station id
station_names = pd.merge(from_station_name, stations_tbl, left_on='to_station_id', right_on='ID')

# Select the columns you want to use.
df = station_names[['Station Name_x', 'Station Name_y', 'gender', 'tripduration']]
# Change tripduration to a numeric value
df["tripduration"] = pd.to_numeric(df["tripduration"], errors = 'coerce')
df_trips = df.astype({"Station Name_x": str, "Station Name_y": str, "gender": str, "tripduration": float})

# Drop rows with NAN's
df_trips = df.dropna()

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    return render_template('index.html')
    # """List all available api routes."""
    # return (
    #     f"Available Routes:<br/>"
    #     f"/api/v1.0/stations<br/>"
    #     f"/api/v1.0/trips<br/>"
    # )


# John are you uisng this route?????
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all stations
    results = session.query(Stations.trip_id).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# John are you uisng this route?????
@app.route("/api/v1.0/trips")
def trips():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all trips data
    results = session.query(Trips.trip_id, Trips.station_from_id, Trips.station_to_id).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_trips
    all_trips = []
    for trip_id, station_from_id, station_to_id in results:
        trips_dict = {}
        trips_dict["trip_id"] = trip_id
        trips_dict["station_from_id"] = station_from_id
        trips_dict["station_to_id"] = station_to_id
        all_trips.append(trips_dict)

    return jsonify(all_trips)

@app.route("/station")
def station():
    return render_template('bike.html')

@app.route("/bikerack")
def rack():
    return render_template('bikerack.html')

@app.route("/biketrip")
def trip_data():
    """Return station, start time and end time""" """Utilized lesson 15.3 activity 03 emojies as an example"""

    # Query for the top 10 emoji data
    results = db.session.query(hist_trips.from_station_id, hist_trips.to_station_id, hist_trips.tripduration).\
        order_by(Trips_DataFrame.from_station_id.desc()).\
        limit(10).all()
    df = pd.DataFrame(results, columns=['from_station_id', 'start_time'])

    # Format the data for Plotly
    plot_trace = {
        "x": df["from_station_id"].values.tolist(),
        "y": df["start_time"].values.tolist(),
        "type": "bar"
    }
    return jsonify(plot_trace)

@app.route("/example")
def trip_example():
    # Capture all data from the hist_trips table inside hist_trips.sqlite
    riders_tbl = pd.read_sql("SELECT * FROM hist_trips", con=engine)

    # Capture alld data from the stations table inside hist_trips.sqlite
    stations_tbl = pd.read_sql("SELECT * FROM stations", con=engine)



if __name__ == '__main__':
    app.run(debug=True)