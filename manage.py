from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
scheduler = APScheduler()

DB_URL = 'postgresql://postgres:postgres@localhost/exchange_rates'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "secret-key"
# app.config["SQLALCHEMY_ECHO"] = True
# app.config["SQLALCHEMY_RECORD_QUERIES"] = True

db = SQLAlchemy(app)
