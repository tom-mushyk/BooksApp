from flask import Blueprint, render_template, url_for, redirect
from app.forms import SearchForm, AddBookForm, ImportBookForm
from app.models import db, Book

books = Blueprint('books', __name__, template_folder='templates')

@books.route('/books', methods=['GET', 'POST'])
def books_route():
    books = Book.query.all()
    form = SearchForm()
    if form.validate_on_submit():
        if form.select.data == 'title':
            books = Book.query.filter_by(title=form.text.data)
            return render_template('books.html', form=form, books=books)
        elif form.select.data == 'authors':
            books = Book.query.filter_by(authors=form.text.data)
            return render_template('books.html', form=form, books=books)
        elif form.select.data == 'language':
            books = Book.query.filter_by(language=form.text.data)
            return render_template('books.html', form=form, books=books)
        elif form.select.data == 'publishedDate':
            books = Book.query.filter_by(publishedDate=form.text.data)
            return render_template('books.html', form=form, books=books)

    else:
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

@books.route('/import', methods=['GET', 'POST'])
def import_route():
    form = ImportBookForm()

    if form.validate_on_submit():
        #api_key = 'AIzaSyDDy0-CvA1TiI99S23MEJp5k_ogkpI1diA'
        # url = 'https://www.googleapis.com/books/v1/volumes?q={}+inauthor:keyes&key=yourAPIKey'.format(form.keyword.data)
        pass


    return render_template('import.html', form=form)

