import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
import datetime as dt
# Import Flask
# from flask import Flask, jsonify
from flask import Flask, render_template, redirect, url_for, jsonify
# app = Flask(__name__, template_folder="templates")
#################################################
# Database Setup
#################################################
# Source:  https://stackoverflow.com/questions/39407254/how-to-set-the-primary-key-when-writing-a-pandas-dataframe-to-a-sqlite-database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine, reflect=True)
print(base.classes.keys())
# Save references to each table
measurement = base.classes.measurement
Station = base.classes.station
# Create an app
app = Flask(__name__)
# app = Flask(__name__, template_folder='templates')
# app = Flask(__name__, static_folder="static")
# Define static routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Weather Api<br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt; start &gt;<br/>"
        f"/api/v1.0/&lt; start &gt;/&lt; end &gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
# Create our session (link) from Python to the DB
    session = Session(engine)
    # Find lastest date
    lastest_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    lastest_year = int(lastest_date[0][:4])
    lastest_month = int(lastest_date[0][5:7])
    lastest_day = int(lastest_date[0][-2:])
    lastest_date
    # Find oldest date
    oldest_date = dt.date(lastest_year, lastest_month, lastest_day) - dt.timedelta(days=365)
    oldest_date
    # Query database
    precipitation = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > oldest_date).\
    order_by(measurement.date).all()

    session.close()
    # Build response
    preciparraymap = []

    for date,prcp in precipitation:
        precipdictmap = {}
        precipdictmap["date"] = date
        precipdictmap["precip"] = prcp
        preciparraymap.append(precipdictmap)
    return jsonify(preciparraymap)

@app.route("/api/v1.0/stations")
def stations():
# Create our session (link) from Python to the DB
    session = Session(engine)
    # Query station table
    station_query =  session.query(Station.station, Station.name, Station.latitude, Station.longitude).\
    order_by(Station.station).all()

    session.close()
    # Build response
    stationarraymap = []

    for station, name, latitude, longitude in station_query:
        stationdictmap = {}
        stationdictmap["Station"] = station
        stationdictmap["Name"] = name
        stationdictmap["Lat"] = latitude
        stationdictmap["Long"] = longitude
        stationarraymap.append(stationdictmap)
    return jsonify(stationarraymap) 

@app.route("/api/v1.0/tobs")
def tobs():
# Create our session (link) from Python to the DB
    session = Session(engine)
    # find most active station
    max_active_station = session.query(measurement.station).\
    group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()
    # find date range for last 12 months for most active station
    lastest_date2 = session.query(measurement.date).\
    filter(measurement.station == max_active_station[0]).order_by(measurement.date.desc()).first()
    lastest_year2 = int(lastest_date2[0][:4])
    lastest_month2 = int(lastest_date2[0][5:7])
    lastest_day2 = int(lastest_date2[0][-2:])
    lastest_date2

    # Calculate the date 1 year ago from the last data point for most active station in the database
    oldest_date2 = dt.date(lastest_year2, lastest_month2, lastest_day2) - dt.timedelta(days=365)
    oldest_date2

    # Perform a query to retrieve the data and temp scores
    tobs_query = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date > oldest_date2).\
    filter(measurement.station == max_active_station[0]).\
    order_by(measurement.date).all()
    session.close()

    # Build response
    tobsarraymap = []

    for date,tobs in tobs_query:
        tobsdictmap = {}
        tobsdictmap["date"] = date
        tobsdictmap["temp"] = tobs
        tobsarraymap.append(tobsdictmap)
    return jsonify(tobsarraymap)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def StartEnd(start,end=0):

    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query station table
    # Without end date
    if end == 0:
        temp_query = session.query(func.min(measurement.tobs),func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date > start).all()
    # With end date
    else:
        temp_query = session.query(func.min(measurement.tobs),func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date > start, measurement.date < end).all()

    session.close()
    # Build response
    temparraymap = []

    for tmin, tmax, tavg in temp_query:
        tempdictmap = {}
        tempdictmap["TMIN"] = tmin
        tempdictmap["TMAX"] = tmax
        tempdictmap["TAVG"] = tavg
        temparraymap.append(tempdictmap)
    return jsonify(temparraymap)  




if __name__ == "__main__":
    app.run(debug=True)