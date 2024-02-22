from app import db
from datetime import datetime

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    status = db.Column(db.String(10))
    created_on = db.Column(db.DateTime, default=datetime.now)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    company_name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    date_of_joining = db.Column(db.Date)
    last_date = db.Column(db.Date)
