import os

import sqlalchemy

from db_models.db_session import db
from web import app

if __name__ == '__main__':
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
        while True:
            try:
                db.create_all()
                break
            except sqlalchemy.exc.OperationalError:
                pass

    app.run(debug=False, host='0.0.0.0', port=3000)
