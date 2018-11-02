from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, DecimalField, PasswordField, BooleanField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Optional, NumberRange, ValidationError


def year_check(form, field):
    if len(field.data) != 4:
        raise ValidationError('Champ à 4 caractères !')

def month_check(form,field):
    x=0
    try :
        x=int(field.data)
    except:
        raise ValidationError('1 - 12 !')
    if x<1 or x>12:
        raise ValidationError('1 - 12 !')

def day_check(form,field):
    x=0
    try :
        x=int(field.data)
    except:
        raise ValidationError('Entrer un nombre !')
    if x<1 or x>31:
        raise ValidationError('1 - 31 !')

def hour_check(form,field):
    x=0
    try :
        x=int(field.data)
    except:
        raise ValidationError('Entrer un nombre !')
    if x<0 or x>23:
        raise ValidationError('0 - 23 !')

def minute_check(form,field):
    x=0
    try :
        x=int(field.data)
    except:
        raise ValidationError('Entrer un nombre !')
    if x<0 or x>60:
        raise ValidationError('0 - 59 !')

def personnel_check(form,field):
    x=field.data
    if len(x)!=2:
        raise ValidationError('2 personnes sont nécessaires pour assurer ce poste')

class AirportCreationForm(FlaskForm):
    code = StringField('Code de l\'aéroport', validators=[DataRequired()])
    nom = StringField('Nom de l\'aéroport', validators=[DataRequired()])
    submit = SubmitField('Valider')


class EmployeeCreationForm(FlaskForm):
    numero_securite_sociale=IntegerField('Numéro de sécurité sociale', validators=[DataRequired()])
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    adresse = StringField('Adresse', validators=[DataRequired()])
    ville = StringField('Ville', validators=[DataRequired()])
    pays = StringField('Pays', validators=[DataRequired()])
    salaire = DecimalField(places=2, validators=[DataRequired()])
    type = SelectField('Type',choices=[('naviguant', 'Naviguant'), ('au_sol', 'Au sol')],validators=[DataRequired()])
    submit = SubmitField('Valider')

class NaviguantCreationForm(FlaskForm):
    nbr_heures_vol = IntegerField('Nombre d\'heures de vol', validators=[DataRequired()])
    fonction = SelectField('Type',choices=[('pilote', 'Pilote'), ('steward', 'Steward'), ('hotesse', 'Hôtesse')],validators=[DataRequired()])
    num_licence_pilote = IntegerField('Numéro de licence',validators=[Optional()])
    submit = SubmitField('Valider')

class VolCreationForm(FlaskForm):
    num_vol = StringField('Numéro de vol', validators=[DataRequired()])
    ts_annee_depart = StringField('Année', validators=[DataRequired(),year_check])
    ts_mois_depart = StringField('Mois', validators=[DataRequired(),month_check])
    ts_jour_depart = StringField('Jour', validators=[DataRequired(),day_check])
    ts_heure_depart = StringField('Heure', validators=[DataRequired(),hour_check])
    ts_minute_depart = StringField('Minute', validators=[DataRequired(),minute_check])
    ts_annee_arrivee = StringField('Année', validators=[DataRequired(),year_check])
    ts_mois_arrivee = StringField('Mois', validators=[DataRequired(),month_check])
    ts_jour_arrivee = StringField('Jour', validators=[DataRequired(),day_check])
    ts_heure_arrivee = StringField('Heure', validators=[DataRequired(),hour_check])
    ts_minute_arrivee = StringField('Minute', validators=[DataRequired(),minute_check])
    immatriculation_appareil = SelectField('Immatriculation des appareils disponibles', validators=[DataRequired()])
    submit = SubmitField('Valider')

class DepartCreationForm(FlaskForm):
    num_vol = SelectField('Numéros de vol disponibles', validators=[DataRequired()])
    id_liaison = SelectField('Liaison effectuée', validators=[DataRequired()])
    pilotes = SelectMultipleField('Pilotes disponibles',validators=[DataRequired()])
    equipages = SelectMultipleField('Membres d\'équipage disponibles', validators=[DataRequired(),personnel_check])
    submit = SubmitField('Valider')
