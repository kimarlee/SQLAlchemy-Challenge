# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
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
    return(
        f"Welcome to Hawaii Climate API!<br/>"
        f"Available Routes: <br/>"
        f"/api.v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end> <br/>"
        f"<p>'start' and 'end date should be in the format MMDDYYY.</p"
    )

@app.route("/api.v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    session.close()

    prcp_list = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station).all()
    session.close()
    station_list = list(np.ravel(stations))
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs(): 
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.tobs).\
                        filter(Measurement.station == "USC00519281").\
                        filter(Measurement.date >= prev_year).all()
    session.close()

    temps = list(np.ravel(tobs_data))

    return jsonify(temps)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start = None, end = None):
    session = Session(engine)
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if end == None: 
        start_data = session.query(*sel).\
                    filter(Measurement.date >= start).all()
        start_list = list(np.ravel(start_data))

        return jsonify(start_list)
    else: 
        start_end_data = session.query(*sel).\
                    filter(Measurement.date >= start).\
                    filter(Measurement.date <= end).all()
        start_end_list = list(np.ravel(start_end_data))

        return jsonify(start_end_list)
    
    session.close()

if __name__ == '__main__':
    app.run(debug=True)