import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
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
        f"Available Routes: :<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )


if __name__ == "__main__":
    app.run(debug=True)