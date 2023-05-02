from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)

class Calibration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #description = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cross_position_x_side = db.Column(db.Float, nullable=False)
    cross_position_y_side = db.Column(db.Float, nullable=False)
    ball_radius_side = db.Column(db.Float, nullable=False)
    cross_position_x_floor = db.Column(db.Float, nullable=False)
    cross_position_y_floor = db.Column(db.Float, nullable=False)
    ball_radius_floor = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Calibration('{self.name}', '{self.date}')"
    
class Throw(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    velocity = db.Column(db.Float, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    accuracy_x = db.Column(db.Float, nullable=False)  # Add this line
    accuracy_y = db.Column(db.Float, nullable=False)  # Add this line
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Throw('{self.id}', '{self.velocity}', '{self.distance}', '{self.date}', '{self.accuracy_x}', '{self.accuracy_y}')"
