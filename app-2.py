import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///data/hist_trips.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Trips = Base.classes.hist_trips
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


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



if __name__ == '__main__':
    app.run(debug=True)