from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    keyword = StringField('Search')
    select = SelectField('Search by', choices=[('title', 'Title'), ('authors', 'Authors'), ('language', 'Language'), ('publishedDate', 'Published date')])
    fromDate = DateField('From date', format='%Y-%m-%d')
    toDate = DateField('To date', format='%Y-%m-%d')
    submit = SubmitField('Find your book')

class AddBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Authors', validators=[DataRequired()])
    publishedDate = DateField('Published Date', validators=[DataRequired()])
    industryIdentifiers = StringField('Industry identifiers', validators=[DataRequired()])
    pageCount = IntegerField('Page count', validators=[DataRequired()])
    imageLinks = StringField('Image links', validators=[DataRequired()])
    language = StringField('Language', validators=[DataRequired()])
    submit = SubmitField('Add book')

class ImportBookForm(FlaskForm):
    keyword = StringField('Search', validators=[DataRequired()])
    title = StringField('Title')
    author = StringField('Author')
    publisher = StringField('Publisher')
    subject = StringField('Subject')
    isbn = StringField('ISBN')
    lccn = StringField('LCCN')
    oclc = StringField('OCLC')
    submit = SubmitField('Find books to import')
