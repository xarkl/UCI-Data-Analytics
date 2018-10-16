import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station 

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    #List available api routes
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    chosen_date = "2017-07-31"
    year,month,day = chosen_date.split('-')
    query_date = dt.date(int(year),int(month),int(day)) - dt.timedelta(days=365)

    results_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > query_date).all()

    all_prcp = []
    for result in results_prcp:
        prcp_dict = {}
        prcp_dict['name'] = result.date
        prcp_dict['prcp'] = result.prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results_station = session.query(Station.station).all()
    station_list = list(np.ravel(results_station))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)

    chosen_date = "2017-07-31"
    year,month,day = chosen_date.split('-')
    query_date = dt.date(int(year),int(month),int(day)) - dt.timedelta(days=365)

    results_temp = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
    filter(Measurement.date > query_date).all()

    all_temps = []
    for result in results_temp:
        temp_dict = {}
        temp_dict["date"] = result.date
        temp_dict["temp"] = result.tobs
        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs).\
    func.max(Measurement.tobs)).filter(Measurement.date > start).all()

    temp_start = list(np.ravel(results))

    return jsonify(temp_start)

if __name__ == '__main__':
     app.run(debug=True)   

