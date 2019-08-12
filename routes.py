from flask import Blueprint, render_template, url_for, redirect, jsonify, abort, flash, get_flashed_messages
from flask_api import status
from forms import SearchForm, AddBookForm, ImportBookForm
from models import db, Book
import requests
from datetime import datetime
import ast

books = Blueprint('books', __name__, template_folder='templates')
api = Blueprint('api', __name__)

#-------------------- APP ROUTES ----------------------


@books.route('/', methods=['GET', 'POST'])
@books.route('/books', methods=['GET', 'POST'])
def books_route():
    form = SearchForm()
    books = Book.query.all()

    if form.validate_on_submit:
        if form.select.data == 'title':
            query = "SELECT * FROM book WHERE title LIKE '%{}%' COLLATE NOCASE;".format(form.keyword.data)
            books = db.engine.execute(query)
        elif form.select.data == 'authors':
            query = "SELECT * FROM book WHERE authors LIKE '%{}%' COLLATE NOCASE;".format(form.keyword.data)
            books = db.engine.execute(query)
        elif form.select.data == 'language':
            query = "SELECT * FROM book WHERE language LIKE '%{}%' COLLATE NOCASE;".format(form.keyword.data)
            books = db.engine.execute(query)

        elif form.select.data == 'publishedDate':
            fromDate = form.fromDate.data
            toDate = form.toDate.data
            print(fromDate)
            query = "SELECT * FROM book WHERE publishedDate BETWEEN '{} 00:00:00' AND '{} 00:00:00'".format(fromDate,toDate)
            books = db.engine.execute(query)



    return render_template('books.html', form=form, books=books)

   # else:
    #    return render_template('books.html', form=form, books=books)

@books.route('/add', methods=['GET', 'POST'])
def add_route():
    form = AddBookForm()

    if form.validate_on_submit():
        book = Book()
        book.title = form.title.data

        authors = str(form.authors.data).split(',')
        book.authors = str(authors)

        book.publishedDate = form.publishedDate.data

        identifiers = str(form.industryIdentifiers.data).split(',')
        listOfDicts = []
        for identifier in identifiers:
            listOfItems = identifier.split(':')
            dictItems = {}
            dictItems['type'] = listOfItems[0]
            dictItems['identifier'] = listOfItems[1]
            listOfDicts.append(dictItems)

        book.industryIdentifiers = str(listOfDicts)
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


        booksToImport = []

        for i in range(0, len(data)):

            id = data[i]['id']

            pageCount = '-'
            if 'pageCount' in data[i]['volumeInfo'].keys():
                pageCount = data[i]['volumeInfo']['pageCount']

            imageLinks = '-'
            if 'imageLinks' in data[i]['volumeInfo'].keys():
                imageLinks = data[i]['volumeInfo']['imageLinks']

            authors = ''
            if 'authors' in data[i]['volumeInfo'].keys():
                for item in data[i]['volumeInfo']['authors']:
                    authors = authors + '{}, '.format(item)


            publishedDate = '-'
            if 'publishedDate' in data[i]['volumeInfo'].keys():
                publishedDate = str(data[i]['volumeInfo']['publishedDate'])

            industryIdentifiers = ''
            if 'industryIdentifiers' in data[i]['volumeInfo'].keys():
                for item in data[i]['volumeInfo']['industryIdentifiers']:

                    industryIdentifiers = industryIdentifiers + '{}:{}, '.format(item['type'], item['identifier'])

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
                'language' : language,
                'id' : id
            })

            print(booksToImport)

        return render_template('import.html', form=form, books=booksToImport)
    else:

        return render_template('import.html', form=form)

@books.route('/importBook/<string:id>', methods=['GET', 'POST'])
def importBook(id):
    url = 'https://www.googleapis.com/books/v1/volumes/{}'.format(id)
    print(url)
    response = requests.get(url)
    data = response.json()

    book = Book()

    if 'title' in data['volumeInfo'].keys():
        book.title = data['volumeInfo']['title']

    if 'authors' in data['volumeInfo'].keys():
        book.authors = str(data['volumeInfo']['authors'])

    if 'publishedDate' in data['volumeInfo'].keys():
        if len(data['volumeInfo']['publishedDate']) > 7:
            year = data['volumeInfo']['publishedDate'][0:4]
            month = data['volumeInfo']['publishedDate'][5:7]
            day = data['volumeInfo']['publishedDate'][8-10]
            book.publishedDate = datetime(year=int(year), month=int(month), day=int(day))

        elif (len(data['volumeInfo']['publishedDate']) < 8) and (len(data['volumeInfo']['publishedDate']) > 4):
            year = data['volumeInfo']['publishedDate'][0:4]
            month = data['volumeInfo']['publishedDate'][5:7]
            book.publishedDate = datetime(year=int(year), month=int(month), day=1)
        elif len(data['volumeInfo']['publishedDate']) == 4:
            year = data['volumeInfo']['publishedDate']
            book.publishedDate = datetime(year=int(year), month=1, day=1)
    if 'industryIdentifiers' in data['volumeInfo'].keys():
        book.industryIdentifiers = str(data['volumeInfo']['industryIdentifiers'])

    if 'pageCount' in data['volumeInfo'].keys():
        book.pageCount = data['volumeInfo']['pageCount']

    if 'imageLinks' in data['volumeInfo'].keys():
        for item in data['volumeInfo']['imageLinks'].values():
            book.imageLinks = item
            break;

    if 'language' in data['volumeInfo'].keys():
        book.language = data['volumeInfo']['language']

    try:
        db.session.add(book)
        db.session.commit()
        print('Book added successfully!')
        return redirect(url_for('.books_route'))

    except:
        print('Cant add this book!')
        return redirect(url_for('.books_route'))



# ---------------- API ROUTES --------------------------

@api.route('/api')
def get_api_docs():
        return render_template('api.html')

@api.route('/api/v1.0/books')
def get_books():

    books = Book.query.all()
    listOfBooks = []
    for book in books:
        publishedDate = book.publishedDate
        publishedDate = str(publishedDate)[0:10]

        listOfBooks.append({
            'id' : book.id,
            'title': book.title,
            'authors': ast.literal_eval(book.authors),
            'publishedDate': publishedDate,
            'industryIdentifiers': ast.literal_eval(book.industryIdentifiers),
            'pageCount': book.pageCount,
            'imageLinks': book.imageLinks,
            'language': book.language

        })

    if len(books) < 1:
        abort(404)
    else:
        return jsonify(listOfBooks), status.HTTP_200_OK

@api.route('/api/v1.0/books/<string:tag>/<string:value>')
def get_books_by_filter(tag, value):

    books = None

    if(tag == 'title'):
        query = "SELECT * FROM book WHERE title LIKE '%{}%' COLLATE NOCASE;".format(value)
        books = db.engine.execute(query)
    elif(tag == 'authors'):
        query = "SELECT * FROM book WHERE authors LIKE '%{}%' COLLATE NOCASE;".format(value)
        books = db.engine.execute(query)

    elif (tag == 'language'):
        query = "SELECT * FROM book WHERE language LIKE '%{}%' COLLATE NOCASE;".format(value)
        books = db.engine.execute(query)

    if books == None:
        abort(404)


    listOfBooks = []
    for book in books:
        publishedDate = book.publishedDate
        publishedDate = str(publishedDate)[0:10]

        listOfBooks.append({
            'id' : book.id,
            'title': book.title,
            'authors': ast.literal_eval(book.authors),
            'publishedDate': publishedDate,
            'industryIdentifiers': ast.literal_eval(book.industryIdentifiers),
            'pageCount': book.pageCount,
            'imageLinks': book.imageLinks,
            'language': book.language

        })

    if len(listOfBooks) < 1:
        abort(404)

    else:
        return jsonify(listOfBooks)

@api.route('/api/v1.0/books/<int:bookid>')
def get_books_by_id(bookid):
    books = Book.query.filter_by(id=bookid)
    bookItem = []
    for book in books:
        publishedDate = book.publishedDate
        publishedDate = str(publishedDate)[0:10]

        bookItem.append({
            'id': book.id,
            'title': book.title,
            'authors': ast.literal_eval(book.authors),
            'publishedDate': publishedDate,
            'industryIdentifiers': ast.literal_eval(book.industryIdentifiers),
            'pageCount': book.pageCount,
            'imageLinks': book.imageLinks,
            'language': book.language

        })

    if len(bookItem) < 1:
        abort(404)
    else:
        return jsonify(bookItem), status.HTTP_200_OK

@api.route('/api/v1.0/books/date/<string:fromDate>/<string:toDate>')
def get_books_by_date(fromDate, toDate):
    query = "SELECT * FROM book WHERE publishedDate BETWEEN '{} 00:00:00' AND '{} 00:00:00'".format(fromDate, toDate)
    books = db.engine.execute(query)
    bookItems = []

    for book in books:
        publishedDate = book.publishedDate
        publishedDate = str(publishedDate)[0:10]

        bookItems.append({
            'id': book.id,
            'title': book.title,
            'authors': ast.literal_eval(book.authors),
            'publishedDate': publishedDate,
            'industryIdentifiers': ast.literal_eval(book.industryIdentifiers),
            'pageCount': book.pageCount,
            'imageLinks': book.imageLinks,
            'language': book.language

        })

    if len(bookItems) < 1:
        abort(404)
    else:
        return jsonify(bookItems), status.HTTP_200_OK


@api.errorhandler(404)
def items_not_found(e):
    return jsonify('Not found :('), status.HTTP_404_NOT_FOUND
