from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField,  TextAreaField
from wtforms.validators import DataRequired


class NewPost(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    content = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Submit')
