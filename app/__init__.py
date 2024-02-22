from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/mydatabase'
app.config['SECRET_KEY'] = "\x16\n'\x89b:\x85\xe0\xfbL\xa92Y \x03\x17"

db = SQLAlchemy(app)

from app import routes
