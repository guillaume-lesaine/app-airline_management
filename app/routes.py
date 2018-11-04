from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import AirportCreationForm, EmployeeCreationForm, NaviguantCreationForm, VolCreationForm, DepartCreationForm, GestionForm
from flask_mysqldb import MySQL

mysql=MySQL(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/gestion', methods=['GET', 'POST'])
def gestion():
    form=GestionForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT numero_securite_sociale, nom, prenom FROM employes")
    employes = [{'numero_securite_sociale':x[0],'nom':x[1],'prenom':x[2]} for x in cur.fetchall()]
    cur.execute("SELECT num_vol FROM vols")
    vols = [{'num_vol':x[0]} for x in cur.fetchall()]
    return render_template('gestion.html', title='Gestion',form=form,employes=employes,vols=vols)

@app.route('/get_suppression', methods=['POST'])
def get_suppression():
    print(request.get_json())
    return('')

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

###
# Vol : réglage technique (temps + géographie)
# Départ : réglage humain
@app.route('/creation/vol', methods=['GET', 'POST'])
def creation_vol():
    cur = mysql.connection.cursor()
    cur.execute("SELECT num_immatriculation FROM appareils")
    data = [x[0] for x in cur.fetchall()]
    choices_immatriculation_appareil=[('',' - ')]+[(x,x) for x in data]
    form = VolCreationForm()
    form.immatriculation_appareil.choices=choices_immatriculation_appareil
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
        ts_depart=ts_annee_depart+'-'+ts_mois_depart+'-'+ts_jour_depart+' '+ts_heure_depart+':'+ts_minute_depart+':00'
        ts_arrivee=ts_annee_arrivee+'-'+ts_mois_arrivee+'-'+ts_jour_arrivee+' '+ts_heure_arrivee+':'+ts_minute_arrivee+':00'
        cur.execute("INSERT INTO vols(num_vol,ts_depart,ts_arrivee,immatriculation_appareil) VALUES (%s, %s, %s, (SELECT num_immatriculation from appareils where num_immatriculation = %s))",(num_vol,ts_depart,ts_arrivee,immatriculation_appareil))
        mysql.connection.commit()
        cur.close()
        return redirect('/index')
    return render_template('creation_vol.html', title='Création vol', form=form)

@app.route('/creation/depart', methods=['GET', 'POST'])
def creation_depart():
    form = DepartCreationForm()
    cur = mysql.connection.cursor()
    # Définition des vols disponibles (vérifier que le numéro n'est pas déjà affecté)
    cur.execute("SELECT num_vol FROM vols")
    data = [x[0] for x in cur.fetchall()]
    choices_num_vol=[('',' - ')]+[(x,x) for x in data]
    form.num_vol.choices=choices_num_vol
    # Définition des liaisons disponibles
    cur.execute("SELECT l.id_liaison, l.aeroport_origine, l.aeroport_destination, a1.code, a2.code FROM liaisons l JOIN aeroports a1 ON l.aeroport_origine = a1.id_aeroports JOIN aeroports a2 ON l.aeroport_destination = a2.id_aeroports")
    data_request_liaisons = cur.fetchall()
    id_liaison=[str(x[0]) for x in data_request_liaisons]
    code_liaison=[' - '.join((x[3],x[4])) for x in data_request_liaisons]
    choices_liaison=[('',' - ')]+[(id_liaison[i],code_liaison[i]) for i in range(len(data_request_liaisons))]
    form.id_liaison.choices=choices_liaison
    # Définition des pilotes disponibles (trouver les pilotes se trouvant au point de départ)
    cur.execute("SELECT e.numero_securite_sociale, e.nom, e.prenom, e.type, n.nbr_heures_vol, n.fonction FROM employes e JOIN naviguants n ON e.numero_securite_sociale = n.numero_securite_sociale WHERE e.type='naviguant' AND n.fonction='pilote' AND n.nbr_heures_vol < 30")
    data_request_pilotes = cur.fetchall()
    id_pilote=[str(x[0]) for x in data_request_pilotes]
    identite_pilote=[', '.join((x[1],x[2])) for x in data_request_pilotes]
    form.pilotes.choices=[(id_pilote[i],identite_pilote[i]) for i in range(len(data_request_pilotes))]
    # Définition des membres d'équipage disponibles (trouver des membres d'équipage au point de départ)
    cur.execute("SELECT e.numero_securite_sociale, e.nom, e.prenom, e.type, n.nbr_heures_vol, n.fonction FROM employes e JOIN naviguants n ON e.numero_securite_sociale = n.numero_securite_sociale WHERE e.type='naviguant' AND n.fonction!='pilote' AND n.nbr_heures_vol < 30")
    data_request_equipages = cur.fetchall()
    id_equipage=[str(x[0]) for x in data_request_equipages]
    identite_equipage=[', '.join((x[1],x[2])) for x in data_request_equipages]
    form.equipages.choices=[(id_equipage[i],identite_equipage[i]) for i in range(len(data_request_equipages))]
    if form.validate_on_submit():
        num_vol=form.num_vol.data
        pilotes=form.pilotes.data
        pilote_1,pilote_2=int(pilotes[0]),int(pilotes[1])
        equipages=form.equipages.data
        equipage_1,equipage_2=int(equipages[0]),int(equipages[1])
        nbr_places_libres=0
        nbr_places_occupees=0
        liaison=form.id_liaison.data
        cur.execute("INSERT INTO departs(num_vol,pilote_1,pilote_2,equipage_1,equipage_2,nbr_places_libres,nbr_places_occupees,liaison) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(num_vol,pilote_1,pilote_2,equipage_1,equipage_2,nbr_places_libres,nbr_places_occupees,liaison))
        mysql.connection.commit()
        cur.close()
    return render_template('creation_depart.html', title='Création départ', form=form)
