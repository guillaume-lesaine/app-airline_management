from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import AirportCreationForm, EmployeeCreationForm, NaviguantCreationForm, VolCreationForm, DepartCreationForm, GestionForm
from flask_mysqldb import MySQL

mysql=MySQL(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='À propos')

@app.route('/gestion', methods=['GET', 'POST'])
def gestion():
    cur = mysql.connection.cursor()
    form=GestionForm()
    cur.execute("SELECT e.numero_securite_sociale, e.nom, e.prenom, n.fonction FROM employes e JOIN naviguants n ON e.numero_securite_sociale = n.numero_securite_sociale")
    employes = [{'numero_securite_sociale':x[0],'nom':x[1],'prenom':x[2],'fonction':x[3].title()} for x in cur.fetchall()]
    cur.execute("SELECT num_vol,ts_depart,ts_arrivee,liaison FROM vols")
    vols=cur.fetchall()
    vols_display = []
    for vol in vols:
        cur.execute("SELECT a1.code ,a1.pays , a2.code, a2.pays FROM liaisons l JOIN aeroports a1 ON l.aeroport_origine = a1.id_aeroports JOIN aeroports a2 ON l.aeroport_destination = a2.id_aeroports WHERE l.id_liaison = %s",[vol[3]])
        liaison = cur.fetchall()[0]
        print(liaison)
        liaison_display = ' - '.join((liaison[0],liaison[2]))
        vols_display.append({'num_vol':vol[0],'ville_depart':liaison[1],'ts_depart':vol[1],'ville_arrivee':liaison[3],'ts_arrivee':vol[2],'liaison':liaison_display})
    cur.execute("SELECT d.id_departs,d.num_vol,e1.nom,e2.nom,e3.nom,e4.nom FROM departs d JOIN employes e1 ON d.pilote_1 = e1.numero_securite_sociale JOIN employes e2 ON d.pilote_2 = e2.numero_securite_sociale JOIN employes e3 ON d.equipage_1 = e3.numero_securite_sociale JOIN employes e4 ON d.equipage_2 = e4.numero_securite_sociale")
    departs = [{'id_departs':x[0],'num_vol':x[1],'pilotes':x[2]+' - '+x[3],'equipage':x[4]+' - '+x[5]} for x in cur.fetchall()]
    return render_template('gestion.html', title='Gestion',form=form,employes=employes,vols=vols_display,departs=departs)


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
                flash('{} {} apparaît dans le départ numéro {}. Veuillez supprimer ce départ.'.format(prenom_flash,nom_flash,depart_flash))
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
# La primary key des départs empêche de pouvoir ajouter des vols de même numéro à des
# Vol : Numéro + liaison
# Départ : immatriculation_appareil + Personnel + dates
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
        to_flash=[]
        num_vol = form.num_vol.data
        id_liaison = form.id_liaison.data
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
        ts_depart=ts_annee_depart+'-'+ts_mois_depart+'-'+ts_jour_depart+' '+ts_heure_depart+':'+ts_minute_depart+':00'
        ts_arrivee=ts_annee_arrivee+'-'+ts_mois_arrivee+'-'+ts_jour_arrivee+' '+ts_heure_arrivee+':'+ts_minute_arrivee+':00'
        cur.execute("INSERT INTO vols(num_vol,ts_depart,ts_arrivee,liaison) VALUES (%s, %s, %s, %s)",(num_vol,ts_depart,ts_arrivee,id_liaison))
        mysql.connection.commit()
        cur.close()
        return redirect('/index')
    return render_template('creation_vol.html', title='Création vol', form=form)

@app.route('/creation/depart', methods=['GET', 'POST'])
def creation_depart():
    cur = mysql.connection.cursor()
    form = DepartCreationForm()
    # Définition des vols disponibles (vérifier que le numéro n'est pas déjà affecté)
    cur.execute("SELECT num_vol FROM vols")
    data = [x[0] for x in cur.fetchall()]
    choices_num_vol=[('',' - ')]+[(x,x) for x in data]
    form.num_vol.choices=choices_num_vol
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
    # Définition des appareils disponibles
    cur.execute("SELECT num_immatriculation FROM appareils")
    data = [x[0] for x in cur.fetchall()]
    choices_immatriculation_appareil=[('',' - ')]+[(x,x) for x in data]
    form.immatriculation_appareil.choices=choices_immatriculation_appareil
    if form.validate_on_submit():
        num_vol=form.num_vol.data
        pilotes=form.pilotes.data
        pilote_1,pilote_2=int(pilotes[0]),int(pilotes[1])
        equipages=form.equipages.data
        equipage_1,equipage_2=int(equipages[0]),int(equipages[1])
        nbr_places_libres=0
        nbr_places_occupees=0
        immatriculation_appareil = form.immatriculation_appareil.data
        cur.execute("INSERT INTO departs(num_vol,pilote_1,pilote_2,equipage_1,equipage_2,nbr_places_libres,nbr_places_occupees,immatriculation_appareil) VALUES (%s, %s, %s, %s, %s, %s, %s, (SELECT num_immatriculation from appareils where num_immatriculation = %s))",(num_vol,pilote_1,pilote_2,equipage_1,equipage_2,nbr_places_libres,nbr_places_occupees,immatriculation_appareil))
        mysql.connection.commit()
        cur.execute("SELECT ts_depart,ts_arrivee FROM vols WHERE num_vol = %s",[num_vol])
        data=cur.fetchall()[0]
        #print('ts_depart :',data[0])
        #print('ts_arrivee :',data[1])
        ts_depart = int(data[0].strftime('%s'))
        ts_arrivee = int(data[1].strftime('%s'))
        #print('ts_depart epoch :',ts_depart)
        #print('ts_arrivee epoch :',ts_arrivee)
        additional_flying_time = ts_arrivee - ts_depart
        additional_flying_hours = additional_flying_time//3600
        if additional_flying_time%3600 != 0:
            additional_flying_hours+=1
        for x in [pilote_1,pilote_2,equipage_1,equipage_2]:
            #print('Numéro sécurité sociale :',x)
            cur.execute("SELECT nbr_heures_vol FROM naviguants WHERE numero_securite_sociale = %s",[x])
            flying_hours=cur.fetchall()[0][0]
            #print('Old flying_hours :',flying_hours)
            flying_hours=flying_hours+additional_flying_hours
            cur.execute("UPDATE naviguants SET nbr_heures_vol = %s WHERE numero_securite_sociale = %s",(flying_hours,x))
            mysql.connection.commit()
            cur.execute("SELECT nbr_heures_vol FROM naviguants WHERE numero_securite_sociale = %s",[x])
            flying_hours=cur.fetchall()[0][0]
            #print('New flying_hours :',flying_hours)
        cur.close()
        return redirect('/creation/depart_conditions')
    return render_template('creation_depart.html', title='Création départ', form=form)

@app.route('/creation/depart_conditions', methods=['GET', 'POST'])
def creation_depart_conditions():
    return render_template('creation_depart_conditions.html', title='Création départ')

@app.route('/pilotage/personnel', methods=['GET', 'POST'])
def pilotage_personnel():
    return render_template('pilotage_personnel.html', title='Pilotage personnel')
