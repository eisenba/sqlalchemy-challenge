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
station = base.classes.station
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
def station():

if __name__ == "__main__":
    app.run(debug=True)