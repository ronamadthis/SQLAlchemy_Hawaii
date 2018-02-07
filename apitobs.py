# /api/v1.0/precipitation
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, and_

import pandas as pd

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/tobs"
            )


@app.route("/api/v1.0/tobs")
def names():
    
    # Query for the dates and temperature observations from the last year.
    session = Session(engine)
    stmnt = session.query(Measurement.date, Measurement.tobs).filter(and_(Measurement.date >= '2017-01-01',\
          Measurement.date < '2018-12-01')).statement
    df=pd.read_sql_query( stmnt, session.bind)
    df=df.astype(str)
    date=df.date.values
    tobs = df.tobs.values
    tobs_dict=dict(zip(date, tobs))

    return jsonify(tobs_dict)


if __name__ == "__main__":
    app.run(debug=True)