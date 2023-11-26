from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    def __init__(self, formdata=_Auto, **kwargs):
        if "prefix" not in kwargs:
            super().__init__(formdata, prefix=type(self).__name__.lower(), **kwargs)
        else:
            super().__init__(formdata, **kwargs)

    name = StringField("Search", validators=[DataRequired()])
    search = SubmitField("Search")
