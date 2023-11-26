from db_models.db_session import db
from db_models.words import Word


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
