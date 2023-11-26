from db_models.db_session import db


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Word {self.id} {self.word} {self.frequency}>'
