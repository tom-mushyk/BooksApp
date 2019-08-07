from flask import Blueprint, render_template, url_for, redirect
from app.forms import SearchForm, AddBookForm
from app.models import db, Book

books = Blueprint('books', __name__, template_folder='templates')

@books.route('/books', methods=['GET', 'POST'])
def books_route():
    form = SearchForm()
    if form.validate_on_submit():
        if form.select.data == 'title':
            books = Book.query.filter_by(title=form.select.data)
            return render_template('books.html', form=form, books=books)
        elif form.select.data == 'authors':
            books = Book.query.filter_by(authors=form.select.data).all()
            return render_template('books.html', form=form, books=books)
        elif form.select.data == 'language':
            books = Book.query.filter_by(language=form.select.data)
            return render_template('books.html', form=form, books=books)
        elif form.select.data == 'publishedDate':
            books = Book.query.filter_by(publishedDate=form.select.data)
            return render_template('books.html', form=form, books=books)

    else:
        books = Book.query.all()
        return render_template('books.html', form=form, books=books)



@books.route('/add', methods=['GET', 'POST'])
def add_route():
    form = AddBookForm()

    if form.validate_on_submit():
        book = Book()
        book.title = form.title.data
        book.authors = form.authors.data
        book.publishedDate = form.publishedDate.data
        book.industryIdentifiers = form.industryIdentifiers.data
        book.pageCount = form.pageCount.data
        book.imageLinks = form.imageLinks.data
        book.language = form.language.data

        try:
            db.session.add(book)
            db.session.commit()
            print('Book added successfully!')
            return redirect(url_for('/books'))

        except:
            print('Cant add this book!')

    return render_template('add.html', form = form)

