from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, and_

import pandas as pd
import numpy as np

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
        f"/api/v1.0/precipitation"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
       # Query all passengers
    session = Session(engine)
    results = session.query(Measurement.prcp).filter(and_(Measurement.date >= '2017-01-01',\
          Measurement.date < '2018-12-01')).all()

    # Convert list of tuples into normal list using np.ravel
    all_prcp = list(np.ravel(results))

    return jsonify(all_prcp)  

if __name__ == '__main__':
    app.run(debug=True)   