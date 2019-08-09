from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(5000), nullable=True)
    authors = db.Column(db.String(100), nullable=True)
    publishedDate = db.Column(db.DateTime, nullable=True)
    industryIdentifiers = db.Column(db.String(5000), nullable=True)
    pageCount = db.Column(db.Integer, nullable=True)
    imageLinks = db.Column(db.String(5000), nullable=True)
    language = db.Column(db.String(), nullable=True)