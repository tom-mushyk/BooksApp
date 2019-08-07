from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    text = StringField('Search', validators=[DataRequired()])
    select = SelectField('Search by', choices=[('title', 'Title'), ('authors', 'Authors'), ('language', 'Language'), ('publishedDate', 'Published date')])
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