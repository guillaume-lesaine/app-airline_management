from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class AirportCreationForm(FlaskForm):
    name = StringField('Nom de l\'aéroport', validators=[DataRequired()])
    code = StringField('Code de l\'aéroport', validators=[DataRequired()])
    submit = SubmitField('Valider')
