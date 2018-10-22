from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DecimalField, PasswordField, BooleanField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Optional

class AirportCreationForm(FlaskForm):
    code = StringField('Code de l\'aéroport', validators=[DataRequired()])
    nom = StringField('Nom de l\'aéroport', validators=[DataRequired()])
    submit = SubmitField('Valider')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class EmployeeCreationForm(FlaskForm):
    numero_securite_sociale=IntegerField('Numéro de sécurité sociale', validators=[DataRequired()])
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    adresse = StringField('Adresse', validators=[DataRequired()])
    ville = StringField('Ville', validators=[DataRequired()])
    pays = StringField('Pays', validators=[DataRequired()])
    salaire = DecimalField(places=2, validators=[DataRequired()])
    type = SelectMultipleField('Type',choices=[('naviguant', 'Naviguant'), ('au_sol', 'Au sol')],validators=[DataRequired()])
    submit = SubmitField('Valider')

class NaviguantCreationForm(FlaskForm):
    nbr_heures_vol = IntegerField('Nombre d\'heures de vol', validators=[DataRequired()])
    fonction = SelectMultipleField('Type',choices=[('pilote', 'Pilote'), ('steward', 'Steward'), ('hotesse', 'Hôtesse')],validators=[DataRequired()])
    num_license_pilote = IntegerField('Numéro de license',validators=[Optional()])
    submit = SubmitField('Valider')
#
# class SimpleForm(Form):
#     string_of_files = ['one\r\ntwo\r\nthree\r\n']
#     list_of_files = string_of_files[0].split()
#     # create a list of value/description tuples
#     files = [(x, x) for x in list_of_files]
#     example = MultiCheckboxField('Label', choices=files)
