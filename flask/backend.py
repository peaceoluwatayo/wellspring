from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://student_behavior_db_user:uEklECGVh4P7Kaxerxcjq3bMjdGQPtsh@dpg-cu4k3p5umphs738ac3l0-a.oregon-postgres.render.com/student_behavior_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class StudentBehavior(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.String(50), nullable=False)
    student_class = db.Column(db.String(10), nullable=False)
    section = db.Column(db.String(10), nullable=False)
    behavior = db.Column(db.String(100), nullable=False)
    students = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    feedback = db.Column(db.Text, nullable=True)
