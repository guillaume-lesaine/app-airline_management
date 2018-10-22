from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import AirportCreationForm, EmployeeCreationForm, NaviguantCreationForm, VolCreationForm
from flask_mysqldb import MySQL

mysql=MySQL(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/creation/airport', methods=['GET', 'POST'])
def creation_airport():
    form = AirportCreationForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        code = form.code.data
        nom = form.nom.data
        cur.execute("INSERT INTO aeroports(id_aeroports,code,nom) VALUES (DEFAULT, %s, %s)",(code,nom))
        mysql.connection.commit()
        cur.close()
        return redirect('/index')
    return render_template('creation_airport.html', title='Création aéroport', form=form)

@app.route('/creation/employee', methods=['GET', 'POST'])
def creation_employee():
    form = EmployeeCreationForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        numero_securite_sociale = form.numero_securite_sociale.data
        cur.execute("SELECT numero_securite_sociale FROM employes")
        data = [x[0] for x in cur.fetchall()]
        if numero_securite_sociale in data:
            flash('Le numéro de sécurité sociale {} existe déjà dans la base'.format(numero_securite_sociale))
        else :
            nom = form.nom.data
            prenom = form.prenom.data
            adresse = form.adresse.data
            ville = form.ville.data
            pays = form.pays.data
            salaire = form.salaire.data
            type = form.type.data[0]
            flash('{} {} est désormais un employé.'.format(prenom,nom))
            cur.execute("INSERT INTO employes(numero_securite_sociale,nom,prenom,adresse,ville,pays,salaire,type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(numero_securite_sociale,nom,prenom,adresse,ville,pays,salaire,type))
            mysql.connection.commit()
            cur.close()
            if type == 'naviguant':
                return redirect(url_for('creation_employee_naviguant',numero_securite_sociale = numero_securite_sociale))
            else:
                return redirect('/index')
    return render_template('creation_employee.html', title='Création employé', form=form)

@app.route('/creation/employee/naviguant/<numero_securite_sociale>', methods=['GET', 'POST'])
def creation_employee_naviguant(numero_securite_sociale):
    form = NaviguantCreationForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        nbr_heures_vol = form.nbr_heures_vol.data
        fonction = form.fonction.data[0]
        num_licence_pilote = form.num_licence_pilote.data
        cur.execute("SELECT num_licence_pilote FROM naviguants")
        data = [x[0] for x in cur.fetchall()]
        if fonction == 'pilote' and num_licence_pilote == None:
            flash('Un pilote doit avoir un numéro de license')
        else :
            if num_licence_pilote in data:
                flash('Le numéro de licence pilote {} existe déjà dans la base'.format(num_licence_pilote))
            else:
                flash('Un employé naviguant a été créé.')
                cur.execute("INSERT INTO naviguants(numero_securite_sociale,nbr_heures_vol,fonction,num_licence_pilote) VALUES (%s, %s, %s, %s)",(numero_securite_sociale,nbr_heures_vol,fonction,num_licence_pilote))
                mysql.connection.commit()
                cur.close()
                return redirect('/index')
    return render_template('creation_employee_naviguant.html', title='Création employé naviguant', form=form)

@app.route('/creation/vol', methods=['GET', 'POST'])
def creation_vol():
    choix=[('pilote', 'Pilote'), ('steward', 'Steward'), ('hotesse', 'Hôtesse')]
    form = VolCreationForm()
    if form.validate_on_submit():
        to_flash=[]
        num_vol = form.num_vol.data
        ts_annee_depart = form.ts_annee_depart.data
        ts_mois_depart = form.ts_mois_depart.data
        ts_jour_depart = form.ts_jour_depart.data
        ts_heure_depart = form.ts_heure_depart.data
        ts_minute_depart = form.ts_minute_depart.data
        ts_annee_arrivee = form.ts_annee_arrivee.data
        ts_mois_arrivee = form.ts_mois_arrivee.data
        ts_jour_arrivee = form.ts_jour_arrivee.data
        ts_heure_arrivee = form.ts_heure_arrivee.data
        ts_minute_arrivee = form.ts_minute_arrivee.data
        immatriculation_appareil = form.immatriculation_appareil.data
        cur = mysql.connection.cursor()
        cur.execute("SELECT num_immatriculation FROM appareils")
        data = [x[0] for x in cur.fetchall()]
        if immatriculation_appareil not in data:
            flash('Le numéro d\'immatriculation {} n\'existe pas dans la base de données. Veuillez rentrer un numéro valide'.format(immatriculation_appareil))
        else :
            ts_depart=ts_annee_depart+'-'+ts_mois_depart+'-'+ts_jour_depart+' '+ts_heure_depart+':'+ts_minute_depart+':00'
            ts_arrivee=ts_annee_arrivee+'-'+ts_mois_arrivee+'-'+ts_jour_arrivee+' '+ts_heure_arrivee+':'+ts_minute_arrivee+':00'
            cur.execute("INSERT INTO vols(num_vol,ts_depart,ts_arrivee,immatriculation_appareil) VALUES (%s, %s, %s, (SELECT num_immatriculation from appareils where num_immatriculation = %s))",(num_vol,ts_depart,ts_arrivee,immatriculation_appareil))
            mysql.connection.commit()
            cur.close()
            return redirect('/index')
    #     cur = mysql.connection.cursor()
    #     nbr_heures_vol = form.nbr_heures_vol.data
    #     fonction = form.fonction.data[0]
    #     num_licence_pilote = form.num_licence_pilote.data
    #     cur.execute("SELECT num_licence_pilote FROM naviguants")
    #     data = [x[0] for x in cur.fetchall()]
    #     if fonction == 'pilote' and num_licence_pilote == None:
    #         flash('Un pilote doit avoir un numéro de license')
    #     else :
    #         if num_licence_pilote in data:
    #             flash('Le numéro de licence pilote {} existe déjà dans la base'.format(num_licence_pilote))
    #         else:
    #             flash('Un employé naviguant a été créé.')
    #             cur.execute("INSERT INTO naviguants(numero_securite_sociale,nbr_heures_vol,fonction,num_licence_pilote) VALUES (%s, %s, %s, %s)",(numero_securite_sociale,nbr_heures_vol,fonction,num_licence_pilote))
    #             mysql.connection.commit()
    #             cur.close()
    #             return redirect('/index')
    return render_template('creation_vol.html', title='Création vol', form=form)
