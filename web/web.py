import requests
from flask import Flask, render_template
from sqlalchemy import exc

from db_models.db_session import db
from db_models.words import Word
from forms.search import SearchForm
from utils.statistics import get_most_popular_words

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def main_page():
    search = SearchForm()
    if search.validate_on_submit():

        api_url = "http://scrapy:2209/crawl"
        rhymes = requests.post(api_url, json={"word": search.name.data}).json()['message']

        word = Word.query.filter_by(word=search.name.data.lower()).first()
        if word:
            word.frequency += 1
            try:
                db.session.commit()
            except exc.SQLAlchemyError:
                db.session.rollback()

        else:
            word = Word(word=search.name.data.lower(), frequency=1)
            db.session.add(word)
            try:
                db.session.commit()
            except exc.SQLAlchemyError:
                db.session.rollback()

        return render_template("rhymes.html", form=search, rhymes=rhymes)
    return render_template("index.html", form=search, words=get_most_popular_words(limit=40, scale=80, alpha=0.5))
