from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.dialects.postgresql import DATE
import pandas as pd



db = SQLAlchemy()

class Billables(db.Model):
    __tablename__ = 'billables'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer)
    billable_rate = db.Column(db.String())
    project = db.Column(db.String())
    date = db.Column(DATE)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    time_difference = db.Column(db.Integer)
    total_cost = db.Column(db.Integer)

    def __repr__(self):
        return '<id {}>'.format(self.id)


