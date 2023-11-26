import os

from flask import Flask, render_template

from db_models.words import Word
from db_models.db_session import db
from utils.scraper import get_rhymes, get_most_popular_words
from web.forms.search import SearchForm

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
