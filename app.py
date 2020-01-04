import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask_sqlalchemy import SQLAlchemy
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
# The database URI
#################################################
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data/riders.sqlite"

db = SQLAlchemy(app)

# Create our database model
class Riders(db.Model):
    __tablename__ = 'riders'

    id = db.Column(db.Integer, primary_key=True)
    Station_Name_x = db.Column(db.String)
    Station_Name_y = db.Column(db.String)
    Location_x = db.Column(db.String)
    Location_y = db.Column(db.String)
    gender = db.Column(db.String)
    Avg_duration = db.Column
    Trip_counts = db.Column(db.Integer)

    def __repr__(self):
        return '<Riders %r>' % (self.name)


# Create database tables
@app.before_first_request
def setup():
    # Recreate database each time for demo
    # db.drop_all()
    db.create_all()

#################################################
# set up global variables to be used throughout the dashboard
#################################################

# # Capture all data from the hist_trips table inside hist_trips.sqlite
# riders_tbl = pd.read_sql("SELECT * FROM hist_trips", con=engine)

# # Capture alld data from the stations table inside hist_trips.sqlite
# stations_tbl = pd.read_sql("SELECT * FROM stations", con=engine)

# # Join station name on from station id
# from_station_name = pd.merge(riders_tbl, stations_tbl, left_on='from_station_id', right_on='ID')

#  # Peform another join to also add station name for the to station id
# station_names = pd.merge(from_station_name, stations_tbl, left_on='to_station_id', right_on='ID')

# # Select the columns you want to use.
# df = station_names[['Station Name_x', 'Station Name_y', 'gender', 'tripduration']]
# # Change tripduration to a numeric value
# df["tripduration"] = pd.to_numeric(df["tripduration"], errors = 'coerce')
# df_trips = df.astype({"Station Name_x": str, "Station Name_y": str, "gender": str, "tripduration": float})

# # Drop rows with NAN's
# df_trips = df.dropna()

# # Find the average drip duration
# df_trips = df_trips.groupby(['Station Name_x', 'Station Name_y', 'gender']).mean()

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

@app.route("/dashboard/web")
def web():
    return render_template('dashboard.html')

# Json data
@app.route("/dashboard/json")
def stations():
   
    # Query for the top 10 stations
    results = db.session.query(Riders.Station_Name_x, Riders.gender, Riders.Trip_counts).\
        order_by(Riders.Trip_counts.desc()).\
        limit(10).all()

    # Create lists from the query results
    Stationx = [result[0] for result in results]
    gender = [result[1] for result in results]
    counts = [int(result[2]) for result in results]

    # Generate the plot trace
    trace = {
        "x": Stationx,
        "y": counts,
        "type": "bar"
    }
    return jsonify(trace)

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