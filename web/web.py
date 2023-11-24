import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.form import _Auto
from bs4 import BeautifulSoup
import requests
import chompjs

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET")
app.config['SQLALCHEMY_DATABASE_URI'] = ('postgresql+psycopg2://' +
                                         os.getenv("DB_USERNAME") + ':' +
                                         os.getenv("DB_PASSWORD") + '@' +
                                         os.getenv("DB_HOST") + ':' +
                                         os.getenv("DB_PORT") + '/' +
                                         os.getenv("DB_USERNAME"))

# Very bad line of code, but we live in Russia, so...
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Word {self.id} {self.word} {self.frequency}>'


with app.app_context():
    db.create_all()


def get_rhymes(word):
    page = requests.get(f'https://www.rhymezone.com/r/rhyme.cgi?Word={word}&typeofrhyme=adv&loc=advlink')
    soup = BeautifulSoup(page.text, "html.parser")
    rhymes = soup.findAll('script')[7].text
    return chompjs.parse_js_object(rhymes)


class SearchForm(FlaskForm):
    def __init__(self, formdata=_Auto, **kwargs):
        if "prefix" not in kwargs:
            super().__init__(formdata, prefix=type(self).__name__.lower(), **kwargs)
        else:
            super().__init__(formdata, **kwargs)

    name = StringField("Search", validators=[DataRequired()])
    search = SubmitField("Search")


@app.route("/", methods=["POST", "GET"])
def main_page():
    search = SearchForm()
    if search.validate_on_submit():
        rhymes = get_rhymes(search.name.data)
        word = Word.query.filter_by(word=search.name.data.lower()).first()
        if word:
            word.frequency += 1
            db.session.commit()
        else:
            word = Word(word=search.name.data.lower(), frequency=1)
            db.session.add(word)
            db.session.commit()

        return render_template("rhymes.html", form=search, rhymes=rhymes)
    return render_template("index.html", form=search, words=get_most_popular_words(limit=40, scale=80, alpha=0.5))


def get_most_popular_words(limit, scale, alpha=10):
    max_frequency = db.session.query(db.func.max(Word.frequency)).limit(limit).scalar()
    words = Word.query.order_by(Word.frequency.desc()).limit(limit).all()
    result = [{
        'title': 1,
        'text': 'Top searches',
        'size': scale
    }]

    for i, word in enumerate(words):
        normalized_frequency = (word.frequency / max_frequency) ** alpha if max_frequency > 0 else 0

        result.append({
            'title': 0,
            'text': word.word,
            'size': normalized_frequency * scale
        })

    return result
