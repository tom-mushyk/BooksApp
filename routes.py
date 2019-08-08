from flask import Blueprint, render_template, url_for, redirect
from app.forms import SearchForm, AddBookForm, ImportBookForm
from app.models import db, Book
import requests
import json

books = Blueprint('books', __name__, template_folder='templates')

@books.route('/', methods=['GET', 'POST'])
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
    terms = ''

    if form.validate_on_submit():
        #polacz sie z api i zaimportuj
        api_key = 'AIzaSyDDy0-CvA1TiI99S23MEJp5k_ogkpI1diA'

        termsBuilder = {'intitle' : form.title.data,
                        'inauthor' : form.author.data,
                        'inpublisher' : form.publisher.data,
                        'subject' : form.subject.data,
                        'isbn': form.isbn.data,
                        'lccn': form.lccn.data,
                        'oclc': form.oclc.data}

        for key, value in termsBuilder.items():
            if value != "":
                terms = terms+'+{}:{}'.format(key, value)

        url = 'https://www.googleapis.com/books/v1/volumes?q={}{}&key={}'.format(form.keyword.data, terms, api_key)
        print(url)

        response = requests.get(url)
        data = response.json()
        data = list(data['items'])

        print(len(data))

        booksToImport = []

        for i in range(0, len(data)):

            pageCount = '-'
            if 'pageCount' in data[i]['volumeInfo'].keys():
                pageCount = data[i]['volumeInfo']['pageCount']

            imageLinks = '-'
            if 'imageLinks' in data[i]['volumeInfo'].keys():
                imageLinks = data[i]['volumeInfo']['imageLinks']

            authors = '-'
            if 'authors' in data[i]['volumeInfo'].keys():
                for author in data[i]['volumeInfo']['authors']:
                    authors = authors + author + ', '

            publishedDate = '-'
            if 'publishedDate' in data[i]['volumeInfo'].keys():
                publishedDate = data[i]['volumeInfo']['publishedDate']

            industryIdentifiers = '-'
            if 'industryIdentifiers' in data[i]['volumeInfo'].keys():
                industryIdentifiers = data[i]['volumeInfo']['industryIdentifiers']

            title = '-'
            if 'title' in data[i]['volumeInfo'].keys():
                title = data[i]['volumeInfo']['title']

            language = '-'
            if 'language' in data[i]['volumeInfo'].keys():
                language = data[i]['volumeInfo']['language']

            booksToImport.append({
                'title' : title,
                'authors' : authors,
                'publishedDate' : publishedDate,
                'industryIdentifiers' : industryIdentifiers,
                'pageCount' : pageCount,
                'imageLinks' : imageLinks,
                'language' : language

            })

            print(booksToImport)

        return render_template('import.html', form=form, books=booksToImport)
    else:

        return render_template('import.html', form=form)

