import os

import requests
from flask import Flask, render_template

from db_models.words import Word
from db_models.db_session import db
from utils.statistics import get_most_popular_words
from forms.search import SearchForm

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
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/", methods=["POST", "GET"])
def main_page():
    search = SearchForm()
    if search.validate_on_submit():

        api_url = "http://scrapy:2209/crawl"
        rhymes = requests.post(api_url, json={"word": search.name.data}).json()['message']

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
