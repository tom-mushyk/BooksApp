from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    authors = db.Column(db.String(100))
    publishedDate = db.Column(db.DateTime)
    industryIdentifiers = db.Column(db.String(500))
    pageCount = db.Column(db.Integer)
    imageLinks = db.Column(db.String(500))
    language = db.Column(db.String(50))