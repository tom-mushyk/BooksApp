from flask import Flask
from app.models import db, migrate, Book
from app.routes import books, api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'rjkrj29r023jr02'

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(books)
app.register_blueprint(api)



if __name__ == '__main__':
    app.run(debug=True)