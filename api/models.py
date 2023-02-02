from app import db
from sqlalchemy.dialects.postgresql import DATE


class Billables(db.Model):
    __tablename__ = 'results'

    employee_id = db.Column(db.Integer, primary_key=True)
    billable_rate = db.Column(db.String())
    project = db.Column(db.String())
    date = db.Column(DATE)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    time_difference = db.Column(db.Integer)
    total_cost = db.Column(db.Integer)

    def __repr__(self):
        return '<id {}>'.format(self.id)
