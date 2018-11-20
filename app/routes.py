from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import AirportCreationForm, EmployeeCreationForm, NaviguantCreationForm, VolCreationForm, DepartCreationForm, DepartConditionsCreationForm, GestionForm
from flask_mysqldb import MySQL

import datetime

mysql=MySQL(app)

# HTML - Affichage en ligne des menus création et pilotage
# HTML - Rendre la présentation de l'application de l'application dynamique avec un bouton d'aide
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='À propos')

#------- gestion() - Faire un LEFT join de manière à aussi prendre en compte les employés non navigants et ceux incomplets
@app.route('/gestion', methods=['GET', 'POST'])
def gestion():
    cur = mysql.connection.cursor()
    form=GestionForm()
    cur.execute("SELECT e.numero_securite_sociale, e.nom, e.prenom, e.type, n.fonction FROM employes e LEFT JOIN naviguants n ON e.numero_securite_sociale = n.numero_securite_sociale")
    data = cur.fetchall()
    employes = []
    for x in data :
        if x[4]!=None:
            employes.append({'numero_securite_sociale':x[0],'nom':x[1],'prenom':x[2],'type':x[3].title(),'fonction':x[4].title()})
        else :
            employes.append({'numero_securite_sociale':x[0],'nom':x[1],'prenom':x[2],'type':x[3].title(),'fonction':''})
    cur.execute("SELECT num_vol,ts_depart,ts_arrivee,liaison FROM vols")
    vols=cur.fetchall()
    vols_display = []
    for vol in vols:
        cur.execute("SELECT a1.code ,a1.pays , a2.code, a2.pays FROM liaisons l JOIN aeroports a1 ON l.aeroport_origine = a1.id_aeroports JOIN aeroports a2 ON l.aeroport_destination = a2.id_aeroports WHERE l.id_liaison = %s",[vol[3]])
        liaison = cur.fetchall()[0]
        print(liaison)
        liaison_display = ' - '.join((liaison[0],liaison[2]))
        vols_display.append({'num_vol':vol[0],'ville_depart':liaison[1],'ts_depart':vol[1],'ville_arrivee':liaison[3],'ts_arrivee':vol[2],'liaison':liaison_display})
    cur.execute("SELECT d.id_departs,d.num_vol,e1.nom,e2.nom,e3.nom,e4.nom FROM departs d LEFT JOIN employes e1 ON d.pilote_1 = e1.numero_securite_sociale LEFT JOIN employes e2 ON d.pilote_2 = e2.numero_securite_sociale LEFT JOIN employes e3 ON d.equipage_1 = e3.numero_securite_sociale LEFT JOIN employes e4 ON d.equipage_2 = e4.numero_securite_sociale")
    departs = cur.fetchall()
    departs_display = []
    for depart in departs:
        pilote_1,pilote_2 = depart[2:4]
        membre_1,membre_2 = depart[4:6]
        if pilote_2 == None :
            pilote_2 = ''
        if membre_2 == None :
            membre_2 = ''
        departs_display.append({'id_departs':depart[0],'num_vol':depart[1],'pilotes':pilote_1+' - '+pilote_2,'equipage':membre_1+' - '+membre_2})
    return render_template('gestion.html', title='Gestion',form=form,employes=employes,vols=vols_display,departs=departs_display)


@app.route('/get_suppression', methods=['GET','POST'])
def get_suppression():
    print('get_suppression')
    deletion_dictionary=request.get_json()
    deletion_employes=deletion_dictionary['A']
    deletion_vols=deletion_dictionary['B']
    deletion_departs=deletion_dictionary['C']
    cur = mysql.connection.cursor()

    # SUPPRIMER DEPART
    if deletion_departs!=[]:
        query= 'DELETE FROM departs WHERE num_vol IN %s'
        cur.execute(query, [deletion_departs])
        mysql.connection.commit()

    # SUPPRIMER EMPLOYÉ
    # Check if pilote dans départs
    for z in deletion_employes:
        query = 'SELECT * FROM departs WHERE %s in (pilote_1,pilote_2,equipage_1,equipage_2)'
        cur.execute(query, [z])
        tuple_departs=cur.fetchall()
        print(tuple_departs)
        if tuple_departs == ():
            pass
        else:
            deletion_employes.remove(z)
            query = 'SELECT nom,prenom FROM employes WHERE numero_securite_sociale = %s'
            cur.execute(query, [z])
            prenom_flash,nom_flash=cur.fetchall()[0]
            for depart in tuple_departs:
                depart_flash=depart[0]
                flash('{} {} apparaît dans le départ associé au numéro de vol {}. Veuillez supprimer ce départ.'.format(prenom_flash,nom_flash,depart_flash))
    for z in deletion_employes:
        query = 'SELECT * FROM naviguants WHERE numero_securite_sociale = %s'
        cur.execute(query, [z])
        if [x[0] for x in cur.fetchall()] == []:
            pass
        else: # Delete from navigant
            query= 'DELETE FROM naviguants WHERE numero_securite_sociale = %s'
            cur.execute(query, [z])
            mysql.connection.commit()
    # Delete from employé
    print(deletion_employes)
    if deletion_employes!=[]:
        print(deletion_employes)
        query= 'DELETE FROM employes WHERE numero_securite_sociale IN %s'
        cur.execute(query, [deletion_employes])
        mysql.connection.commit()
    return('')

# HTML - Insérer un espace à la fin du form
# HTML - Rendre la consigne dynamique avec un bouton d'aide
# MySQL - Faut-il conserver un champ salaire ?
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
            type = form.type.data
            flash('{} {} est désormais un employé.'.format(prenom,nom))
            cur.execute("INSERT INTO employes(numero_securite_sociale,nom,prenom,adresse,ville,pays,salaire,type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(numero_securite_sociale,nom,prenom,adresse,ville,pays,salaire,type))
            mysql.connection.commit()
            cur.close()
            print('//////',type)
            if type == 'naviguant':
                return redirect(url_for('creation_employee_naviguant',numero_securite_sociale = numero_securite_sociale))
            else:
                return redirect('/index')
    return render_template('creation_employee.html', title='Création employé', form=form)

# NaviguantCreationForm() + HTML - Retirer le champ nombre d'heures de vol
# MySQL - Retirer la colonne du nombre d'heures de vol dans naviguants
# HTML - Valeur par défaut pour choix de la fonction
@app.route('/creation/employee/naviguant/<numero_securite_sociale>', methods=['GET', 'POST'])
def creation_employee_naviguant(numero_securite_sociale):
    form = NaviguantCreationForm()
    choices_fonction=[('',' - '),('pilote','Pilote'),('steward','Steward'),('hôtesse','Hôtesse')]
    form.fonction.choices=choices_fonction
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        nbr_heures_vol = form.nbr_heures_vol.data
        fonction = form.fonction.data
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

#------- VolCreationForm() + HTML - Demander un temps de vol plutôt qu'une date d'arrivée
#------- creation_vol() - Transformer le temps de vol en format date à partir du départ
#------- creation_vol() - Flash message de confirmation de création
#------- creation_vol() - Vérifier que le numéro de vol n'existe pas déjà
# VolCreationForm() - Vérifier que le temps de vol est non nul
@app.route('/creation/vol', methods=['GET', 'POST'])
def creation_vol():
    cur = mysql.connection.cursor()
    form = VolCreationForm()
    # Définition des liaisons disponibles
    cur.execute("SELECT l.id_liaison, l.aeroport_origine, l.aeroport_destination, a1.code, a2.code FROM liaisons l JOIN aeroports a1 ON l.aeroport_origine = a1.id_aeroports JOIN aeroports a2 ON l.aeroport_destination = a2.id_aeroports")
    data_request_liaisons = cur.fetchall()
    id_liaison=[str(x[0]) for x in data_request_liaisons]
    code_liaison=[' - '.join((x[3],x[4])) for x in data_request_liaisons]
    choices_liaison=[('',' - ')]+[(id_liaison[i],code_liaison[i]) for i in range(len(data_request_liaisons))]
    form.id_liaison.choices=choices_liaison
    if form.validate_on_submit():
        num_vol = form.num_vol.data
        cur.execute("SELECT * FROM vols WHERE num_vol = %s",[num_vol])
        data = cur.fetchall()
        if data!=():
            flash('Le numéro de vol {} existe déjà dans la base, veuillez le changer.'.format(num_vol))
        else:
            flash('Le vol numéro {} vient d\'être créé.'.format(num_vol))
            id_liaison = form.id_liaison.data
            ts_annee_depart = int(form.ts_annee_depart.data)
            ts_mois_depart = int(form.ts_mois_depart.data)
            ts_jour_depart = int(form.ts_jour_depart.data)
            ts_heure_depart = int(form.ts_heure_depart.data)
            ts_minute_depart = int(form.ts_minute_depart.data)
            ts_vol = int(form.ts_vol_heures.data)*3600 + int(form.ts_vol_minutes.data)*60
            ts_depart=datetime.datetime(ts_annee_depart,ts_mois_depart,ts_jour_depart,ts_heure_depart,ts_minute_depart,0)
            ts_arrivee = int(ts_depart.strftime('%s')) + ts_vol
            ts_arrivee=datetime.datetime.fromtimestamp(ts_arrivee)
            cur.execute("INSERT INTO vols(num_vol,ts_depart,ts_arrivee,liaison) VALUES (%s, %s, %s, %s)",(num_vol,ts_depart,ts_arrivee,id_liaison))
            mysql.connection.commit()
            cur.close()
            return redirect('/index')
    return render_template('creation_vol.html', title='Création vol', form=form)

# creation_depart() - Permettre de créer un départ sans employé
@app.route('/creation/depart', methods=['GET', 'POST'])
def creation_depart():
    cur = mysql.connection.cursor()
    form = DepartCreationForm()
    cur.execute("SELECT num_vol,ts_depart,ts_arrivee,liaison FROM vols v WHERE v.num_vol NOT IN (SELECT d.num_vol FROM departs d)")
    vols=cur.fetchall()
    vols_display = []
    for vol in vols:
        cur.execute("SELECT a1.code ,a1.pays , a2.code, a2.pays FROM liaisons l JOIN aeroports a1 ON l.aeroport_origine = a1.id_aeroports JOIN aeroports a2 ON l.aeroport_destination = a2.id_aeroports WHERE l.id_liaison = %s",[vol[3]])
        liaison = cur.fetchall()[0]
        liaison_display = ' - '.join((liaison[0],liaison[2]))
        vols_display.append({'num_vol':vol[0],'ville_depart':liaison[1],'ts_depart':vol[1],'ville_arrivee':liaison[3],'ts_arrivee':vol[2],'liaison':liaison_display})
    if form.validate_on_submit():
        selected_vol = request.form.getlist('selection')[0]
        return redirect(url_for('creation_depart_conditions',selected_vol = selected_vol))
    return render_template('creation_depart.html', title='Création départ', vols=vols_display, form=form)

# Requête similaire pour appareils
# Retirer la colonne heures de vol (pas statique)
#------- creation_depart_conditions() - Prendre en compte le temps du départ pour trouver la dernière position la position
# creation_depart_conditions() - Gérer la création d'un départ intermédiaire
@app.route('/creation/depart_conditions/<selected_vol>', methods=['GET', 'POST'])
def creation_depart_conditions(selected_vol):
    cur = mysql.connection.cursor()
    form = DepartConditionsCreationForm()
    # Find the country to be in as well as the time for the departure
    cur.execute("SELECT a.pays,v.ts_depart,v.ts_arrivee FROM vols v JOIN liaisons l ON v.liaison = l.id_liaison JOIN aeroports a ON l.aeroport_origine = a.id_aeroports WHERE v.num_vol = %s",[selected_vol])
    pays_depart,ts_depart,ts_arrivee = cur.fetchall()[0]
    ts_depart_format = ts_depart
    ts_depart = int(ts_depart.strftime('%s'))
    ts_arrivee = int(ts_arrivee.strftime('%s'))
    ts_vol = ts_arrivee - ts_depart
    # Get the list of employees
    cur.execute("SELECT numero_securite_sociale FROM naviguants")
    liste_numero_securite_sociale = [x[0] for x in cur.fetchall()]
    liste_numero_securite_sociale_possibles = liste_numero_securite_sociale.copy()
    print(liste_numero_securite_sociale_possibles)
    pilotes_disponibles, membres_disponibles = [],[]
    # Get the last position of every flying employee
    for x in liste_numero_securite_sociale:
        print('--------',x)
        # Vérifier si l'employé est déjà enregisté sur un vol et déterminer sa position au moment du décolage du départ actuel
        cur.execute("SELECT ts_arrivee,ville_destination,pays_destination FROM departs JOIN vols ON vols.num_vol = departs.num_vol JOIN liaisons ON vols.liaison = liaisons.id_liaison JOIN (SELECT id_aeroports AS id_aeroport_destination, code AS code_destination, nom AS nom_destination, ville AS ville_destination, pays AS pays_destination FROM aeroports) AS aeroports_destination ON liaisons.aeroport_destination = aeroports_destination.id_aeroport_destination WHERE vols.ts_arrivee = (SELECT MAX(ts_arrivee) AS ts_depart_next_flight FROM ((SELECT pilote_1 AS naviguant, ts_arrivee FROM departs JOIN vols ON departs.num_vol = vols.num_vol) UNION (SELECT pilote_2 AS naviguant, ts_arrivee FROM departs JOIN vols ON departs.num_vol = vols.num_vol) UNION (SELECT equipage_1 AS naviguant, ts_arrivee FROM departs JOIN vols ON departs.num_vol = vols.num_vol) UNION (SELECT equipage_2 AS naviguant, ts_arrivee FROM departs JOIN vols ON departs.num_vol = vols.num_vol)) AS total_naviguant WHERE total_naviguant.naviguant = %s AND ts_arrivee < %s GROUP BY naviguant)",(x,ts_depart_format))
        data = cur.fetchall()
        print(data)
        cur.execute("SELECT e.nom,e.prenom,n.fonction,e.ville,e.pays FROM employes e JOIN naviguants n ON e.numero_securite_sociale = n.numero_securite_sociale WHERE e.numero_securite_sociale = %s",[x])
        data_identite = cur.fetchall()
        if data != ():
            print('a')
            nom_employe,prenom_employe,fonction_employe = data_identite[0][:3]
            ts_arrivee_employee, ville_employee, pays_employee = data[0]
            ts_arrivee_employee = int(ts_arrivee_employee.strftime('%s'))
        else :
            print('b')
            nom_employe,prenom_employe,fonction_employe,ville_employee, pays_employee = data_identite[0]
            ts_arrivee_employee = ts_depart # Le pilote est prêt à partir
        # Compter les heures de vol sur les 30 jours précédants le départ
        cur.execute("SELECT v.ts_depart, v.ts_arrivee FROM vols v JOIN departs d ON v.num_vol = d.num_vol WHERE (pilote_1 = %s OR pilote_2 = %s OR equipage_1 = %s OR equipage_2 = %s)",(x,x,x,x))
        flights_employe = cur.fetchall()
        flying_hours = 0
        for z in flights_employe :
            # Si le vol considéré a eu un départ dans les 30 jours précédants l'arrivée du départ en cours de création, comptabilisé les heures de vol
            if (ts_arrivee - 30*24*3600) < int(z[0].strftime('%s')):
                flying_hours = flying_hours + (int(z[1].strftime('%s')) - int(z[0].strftime('%s')))
            else :
                pass
        if pays_employee != pays_depart or (ts_arrivee_employee < (ts_depart - 72*3600) and ts_arrivee_employee!=ts_depart): # Si (le pilote n'est pas dans le pays de départ) ou (qu'il y est mais pas dans les 72 dernières heures et qu'il n'y habite pas)
            liste_numero_securite_sociale_possibles.remove(x)
            print(0)
            print('pays_employee :',pays_employee)
            print('pays_depart :',pays_depart)
        elif flying_hours >= (30*24*3600 - ts_vol): # Si dans les 30 jours précédants l'arrivée du départ actuel, le pilote a fait plus de (30h - durée du vol prévu) ne pas le considérer
            liste_numero_securite_sociale_possibles.remove(x)
            print(1)
        else :
            print(2)
            if fonction_employe == 'pilote':
                pilotes_disponibles.append({'numero_securite_sociale':x,'nom':nom_employe,'prenom':prenom_employe,'fonction':fonction_employe})
            else:
                membres_disponibles.append({'numero_securite_sociale':x,'nom':nom_employe,'prenom':prenom_employe,'fonction':fonction_employe})
    # Définition des appareils disponibles
    cur.execute("SELECT num_immatriculation FROM appareils")
    data = [x[0] for x in cur.fetchall()]
    choices_immatriculation_appareil=[('',' - ')]+[(x,x) for x in data]
    form.immatriculation_appareil.choices=choices_immatriculation_appareil
    if form.validate_on_submit():
        pilotes = request.form.getlist('pilotes')
        nbr_pilotes = len(pilotes)
        membres = request.form.getlist('membres')
        nbr_membres = len(membres)
        immatriculation_appareil = form.immatriculation_appareil.data
        if nbr_pilotes > 2:
            flash('Vous pouvez sélectionner deux pilotes maximum')
        if nbr_membres > 2:
            flash('Vous pouvez sélectionner deux membres d\'équipage maximum')
        if nbr_pilotes == 0:
            flash('Veuillez sélectionner des pilotes')
        if nbr_membres == 0:
            flash('Veuillez sélectionner des membres d\'équipage')
        if nbr_pilotes <= 2 and nbr_membres <= 2 and nbr_pilotes != 0 and nbr_membres != 0:
            flash('Un nouveau départ vient d\'être associé au vol numéro {}'.format(selected_vol))
            if nbr_pilotes == 1 :
                pilotes.append(None)
            if nbr_membres == 1 :
                membres.append(None)
            cur.execute("INSERT INTO departs(num_vol,pilote_1,pilote_2,equipage_1,equipage_2,nbr_places_libres,nbr_places_occupees,immatriculation_appareil) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(selected_vol,pilotes[0],pilotes[1],membres[0],membres[1],0,0,immatriculation_appareil))
            mysql.connection.commit()
            return redirect('/index')
    # Less than 30 hours of flight with addition
    # In the right country at the right moment
    return render_template('creation_depart_conditions.html', title='Création départ', form = form, pilotes_disponibles = pilotes_disponibles,membres_disponibles = membres_disponibles)

# pilotage_personnel() - Ranger vols prévus par ordre de proximité en temps
#------- pilotage_personnel() - Afficher les vols passés
#------- HTML + pilotage_personnel() - Montrer les vols passés
#------- HTML - Afficher nom de la personne quand sélectionnée
#------- HTML - Mettre colonnes à la même taille
@app.route('/pilotage/personnel', methods=['GET', 'POST'])
def pilotage_personnel():
    cur = mysql.connection.cursor()
    cur.execute("SELECT e.numero_securite_sociale,e.nom,e.prenom,n.fonction FROM employes e JOIN naviguants n ON e.numero_securite_sociale = n.numero_securite_sociale")
    employes = cur.fetchall()
    employes_display = []
    prevus_display = {}
    passes_display = {}
    # Request naviguant in flight
    cur.execute("SELECT nom, prenom,fonction,naviguants_vols.naviguant, naviguants_vols.num_vol FROM ((SELECT pilote_1 AS naviguant, num_vol FROM departs) UNION DISTINCT (SELECT pilote_2 AS naviguant, num_vol FROM departs) UNION DISTINCT (SELECT equipage_1 AS naviguant, num_vol FROM departs) UNION DISTINCT (SELECT equipage_2 AS naviguant, num_vol FROM departs)) AS naviguants_vols JOIN vols ON vols.num_vol = naviguants_vols.num_vol JOIN employes ON employes.numero_securite_sociale = naviguants_vols.naviguant JOIN naviguants ON naviguants.numero_securite_sociale = naviguants_vols.naviguant WHERE ts_depart < NOW() AND ts_arrivee > NOW();")
    flying_employes = cur.fetchall()
    vol_en_cours={}
    for employe in employes:

        # Sélectionner si l'employé est en vol
        flying=False
        for x in flying_employes:
            if x[3] == employe[0] :
                print('-----',x[3])
                cur.execute("SELECT a1.code,a2.code,v.ts_depart,v.ts_arrivee FROM vols v JOIN liaisons l ON v.liaison = l.id_liaison JOIN aeroports a1 ON l.aeroport_origine = a1.id_aeroports JOIN aeroports a2 ON l.aeroport_destination = a2.id_aeroports WHERE v.num_vol = %s",[x[4]])
                information_vol = cur.fetchall()[0]
                vol_en_cours[str(employe[0])]={'num_vol':x[4],'liaison':information_vol[0]+' - '+information_vol[1],'ts_depart':information_vol[2],'ts_arrivee':information_vol[3]}
                flying=True
        if not flying:
            vol_en_cours[str(employe[0])]=None
        employes_display.append({'numero_securite_sociale':str(employe[0]),'nom':employe[1].upper(),'prenom':employe[2],'fonction':employe[3]})

        # Sélectionner les départs prévus
        cur.execute("SELECT vols.num_vol, ts_depart, ts_arrivee, code_origine, code_destination FROM departs JOIN vols ON vols.num_vol = departs.num_vol JOIN liaisons ON vols.liaison = liaisons.id_liaison JOIN (SELECT id_aeroports AS id_aeroport_destination, code AS code_destination, nom AS nom_destination FROM aeroports) AS aeroports_destination ON liaisons.aeroport_destination = aeroports_destination.id_aeroport_destination JOIN (SELECT id_aeroports AS id_aeroport_origine, code AS code_origine, nom AS nom_origine FROM aeroports) AS aeroports_origine ON liaisons.aeroport_origine = aeroports_origine.id_aeroport_origine WHERE (departs.pilote_1 = %s OR departs.pilote_2 = %s OR departs.equipage_1 = %s OR departs.equipage_2 = %s) AND ts_depart > NOW();",(employe[0],employe[0],employe[0],employe[0]))
        departs_prevus=cur.fetchall()
        if departs_prevus == ():
            prevus_display[str(employe[0])]=[]
        else :
            departs_prevus_list=[]
            for depart in departs_prevus:
                departs_prevus_list.append({'num_vol':depart[0],'ts_depart':depart[1],'ts_arrivee':depart[2],'liaison':depart[3]+' - '+depart[4]})
            prevus_display[str(employe[0])] = departs_prevus_list

        # Sélectionner les départs passés
        cur.execute("SELECT vols.num_vol, ts_depart, ts_arrivee, code_origine, code_destination FROM departs JOIN vols ON vols.num_vol = departs.num_vol JOIN liaisons ON vols.liaison = liaisons.id_liaison JOIN (SELECT id_aeroports AS id_aeroport_destination, code AS code_destination, nom AS nom_destination FROM aeroports) AS aeroports_destination ON liaisons.aeroport_destination = aeroports_destination.id_aeroport_destination JOIN (SELECT id_aeroports AS id_aeroport_origine, code AS code_origine, nom AS nom_origine FROM aeroports) AS aeroports_origine ON liaisons.aeroport_origine = aeroports_origine.id_aeroport_origine WHERE (departs.pilote_1 = %s OR departs.pilote_2 = %s OR departs.equipage_1 = %s OR departs.equipage_2 = %s) AND ts_arrivee < NOW();",(employe[0],employe[0],employe[0],employe[0]))
        departs_passes=cur.fetchall()
        if departs_passes == ():
            passes_display[str(employe[0])]=[]
        else :
            departs_passes_list=[]
            for depart in departs_passes:
                departs_passes_list.append({'num_vol':depart[0],'ts_depart':depart[1],'ts_arrivee':depart[2],'liaison':depart[3]+' - '+depart[4]})
            passes_display[str(employe[0])] = departs_passes_list
    return render_template('pilotage_personnel.html', title='Pilotage personnel',employes=employes_display,vol_en_cours=vol_en_cours,departs_prevus=prevus_display,departs_passes=passes_display)
