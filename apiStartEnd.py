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


session = Session(engine)

def calc_temp(startDate):
    result = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                         filter(Measurement.date >= startDate).all()
    return result 


def calc_temps(startDate, endDate):
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                         filter(Measurement.date >= startDate, Measurement.date <= endDate).all()
    return results

startDate = input("What is the start date (YYYY-MM-DD)?")
endDate = input("What is the end date(YYYY-MM-DD)?")

if (endDate ==" "):
    @app.route("/")
    def welcome():
        """List all available api routes."""
        return (
            f"Available Routes:<br/>"
            f"/api/v1.0/start<br/>"
        )


    @app.route("/api/v1.0/start")
    def start():
        result = calc_temp(startDate)
        temp = list(np.ravel(result)) 
        return jsonify(temp)  


else:
    @app.route("/")
    def welcome():
        """List all available api routes."""
        return (
            f"Available Routes:<br/>"
            f"/api/v1.0/start_end"
        )


    @app.route("/api/v1.0/start_end")
    def start_end():
        results = calc_temps(startDate, endDate)
        temp = list(np.ravel(results)) 
        return jsonify(temp)


if __name__ == '__main__':
    app.run(debug=True)   
