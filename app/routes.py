from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import AirportCreationForm, EmployeeCreationForm, NaviguantCreationForm, VolCreationForm, DepartCreationForm, DepartConditionsCreationForm, BilletReservationForm, BilletConditionsReservationForm
from flask_mysqldb import MySQL

import datetime
import random
import os

mysql=MySQL(app)

def executeScriptsFromFile(filename,TS_DEPART_NV_VOL,TS_ARRIVEE_NV_VOL,TPS_VOL,NB_HEURES_VOL_NV_VOL,CODE_ORIGINE_NV_VOL,CODE_DESTINATION_NV_VOL):
    cur = mysql.connection.cursor()
    print('ok sql')
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlFile=sqlFile.replace('\n',' ')
    sqlFile=sqlFile.replace('\t',' ')
    sqlCommands = sqlFile.split(';')

    cur.execute('SET @TS_DEPART_NV_VOL = %s',[TS_DEPART_NV_VOL])
    cur.execute('SET @TS_ARRIVEE_NV_VOL = %s',[TS_ARRIVEE_NV_VOL])
    cur.execute('SET @TPS_VOL = %s',[TPS_VOL])
    cur.execute('SET @NB_HEURES_VOL_NV_VOL = %s',[NB_HEURES_VOL_NV_VOL])
    cur.execute('SET @CODE_ORIGINE_NV_VOL = %s',[CODE_ORIGINE_NV_VOL])
    cur.execute('SET @CODE_DESTINATION_NV_VOL = %s',[CODE_DESTINATION_NV_VOL])
    for command in sqlCommands:
        print()
        cur.execute(command)
        if command.strip()[0:6]=='SELECT':
            print(command)
            query = cur.fetchall()
    return(query)

@app.route('/')
@app.route('/accueil')
def accueil():
    return render_template('accueil.html', title='Air Centrale - Accueil')

@app.route('/ressources')
def ressources():
    return render_template('ressources.html', title='Air Centrale - Ressources')

@app.route('/gerer', methods=['GET', 'POST'])
def gerer():
    cur = mysql.connection.cursor()
    # Trouver les employés
    cur.execute("SELECT e.numero_securite_sociale, e.nom, e.prenom, e.type, n.fonction, n.nbr_heures_vol FROM employes e LEFT JOIN naviguants n ON e.numero_securite_sociale = n.numero_securite_sociale")
    data = cur.fetchall()
    employes = []
    for x in data :
        if x[4]!=None:
            employes.append({'numero_securite_sociale':x[0],'nom':x[1].upper(),'prenom':x[2],'type':x[3].title(),'fonction':x[4].title(),'heures_vol':x[5]})
        else :
            employes.append({'numero_securite_sociale':x[0],'nom':x[1].upper(),'prenom':x[2],'type':x[3].title(),'fonction':'','heures_vol':''})
    # Trouver les vols
    cur.execute("SELECT num_vol,ts_depart,ts_arrivee,liaison FROM vols")
    vols=cur.fetchall()
    vols_display = []
    for vol in vols:
        cur.execute("SELECT a1.code ,a1.pays , a2.code, a2.pays FROM liaisons l JOIN aeroports a1 ON l.aeroport_origine = a1.id_aeroports JOIN aeroports a2 ON l.aeroport_destination = a2.id_aeroports WHERE l.id_liaison = %s",[vol[3]])
        liaison = cur.fetchall()[0]
        liaison_display = ' - '.join((liaison[0],liaison[2]))
        vols_display.append({'num_vol':vol[0],'ville_depart':liaison[1],'ts_depart':vol[1],'ville_arrivee':liaison[3],'ts_arrivee':vol[2],'liaison':liaison_display})
    # Trouver les départs
    cur.execute("SELECT d.id_departs,d.num_vol,e1.nom,e2.nom,e3.nom,e4.nom,d.immatriculation,d.nbr_places_libres FROM departs d LEFT JOIN employes e1 ON d.pilote_1 = e1.numero_securite_sociale LEFT JOIN employes e2 ON d.pilote_2 = e2.numero_securite_sociale LEFT JOIN employes e3 ON d.equipage_1 = e3.numero_securite_sociale LEFT JOIN employes e4 ON d.equipage_2 = e4.numero_securite_sociale")
    departs = cur.fetchall()
    departs_display = []
    for depart in departs:
        pilote_1,pilote_2 = depart[2:4]
        membre_1,membre_2 = depart[4:6]
        if pilote_1 == None :
            pilote_1 = ''
        if membre_1 == None :
            membre_1 = ''
        if pilote_2 == None :
            pilote_2 = ''
        if membre_2 == None :
            membre_2 = ''
        departs_display.append({'id_departs':depart[0],'num_vol':depart[1],'pilotes':pilote_1.upper()+' - '+pilote_2.upper(),'equipage':membre_1.upper()+' - '+membre_2.upper(),'immatriculation':depart[6],'nbr_places_libres':depart[7]})
    # Trouver les passagers
    cur.execute("SELECT id_passager,nom,prenom,pays FROM passagers")
    passagers=cur.fetchall()
    passagers_display = []
    for passager in passagers:
        passagers_display.append({'id_passager':passager[0],'nom':passager[1].upper(),'prenom':passager[2],'pays':passager[3]})
    # Trouver les billets
    cur.execute("SELECT b.num_billet,b.num_depart,p.nom,p.prenom FROM billets b JOIN passagers p ON b.num_passager = p.id_passager")
    billets=cur.fetchall()
    billets_display = []
    for billet in billets:
        billets_display.append({'num_billet':billet[0],'num_depart':billet[1],'client':billet[2].upper() + ' ' + billet[3]})
    return render_template('gerer.html', title='Air Centrale - Gérer',employes=employes,vols=vols_display,departs=departs_display,passagers=passagers_display,billets=billets_display)

@app.route('/get_suppression', methods=['GET','POST'])
def get_suppression():
    # Récupération des données provenant de l'utilisateur
    deletion_dictionary=request.get_json()
    deletion_employes=deletion_dictionary['A']
    deletion_vols=deletion_dictionary['B']
    deletion_departs=deletion_dictionary['C']
    deletion_passagers=deletion_dictionary['D']
    deletion_billets=deletion_dictionary['E']
    cur = mysql.connection.cursor()

    def function_deletion_billets(deletion_billets_list):
        print(deletion_billets_list)
        for billet in deletion_billets_list:
            print('-------',billet) # Augmenter de 1 le nombre de places disponibles dans le départ associé au billet
            cur.execute("UPDATE departs SET nbr_places_libres = nbr_places_libres + 1 WHERE id_departs = (SELECT num_depart FROM billets WHERE num_billet = %s)",[int(billet)])
            mysql.connection.commit()
        format_strings = ','.join(['%s'] * len(deletion_billets_list))
        query= 'DELETE FROM billets WHERE num_billet IN (%s)' % format_strings
        cur.execute(query, tuple(deletion_billets_list))
        mysql.connection.commit()
        flash('Le billet {} a été supprimé. La place est de nouveau disponible.'.format(billet),"alert alert-info")


    def function_deletion_passagers(deletion_passagers_list):
        deletion_passagers_list = [int(x) for x in deletion_passagers_list]
        format_strings = ','.join(['%s'] * len(deletion_passagers_list))
        query = 'SELECT num_billet FROM billets WHERE num_passager IN (%s)' % format_strings
        cur.execute(query, tuple(deletion_passagers_list))
        deletion_billets_list=[x[0] for x in cur.fetchall()]
        for x in deletion_passagers_list:
            flash('Le passager numéro {} a été supprimé. Les places qu\'il occupait sont désormais libérées.'.format(x),"alert alert-info")
        if deletion_billets_list!=[]:
            function_deletion_billets(deletion_billets_list)
        query = 'DELETE FROM passagers WHERE id_passager IN (%s)' % format_strings
        cur.execute(query, tuple(deletion_passagers_list))
        mysql.connection.commit()

    def function_deletion_departs(deletion_departs_list):
        print(deletion_departs_list)
        format_strings = ','.join(['%s'] * len(deletion_departs_list))

        # Trouver les billets qui vont être supprimés
        query = 'SELECT num_billet,num_depart FROM billets WHERE num_depart IN (%s)' % format_strings
        cur.execute(query, tuple([int(x) for x in deletion_departs_list]))
        billets = cur.fetchall()

        # Supprimer les billets
        query = 'DELETE FROM billets WHERE num_depart IN (%s)' % format_strings
        cur.execute(query, tuple(deletion_departs_list))
        mysql.connection.commit()

        #Décrémenter les heures de vol du personnel navigant
        for depart in deletion_departs_list:
            print(depart)
            cur.execute("SELECT v.ts_depart,v.ts_arrivee FROM vols v JOIN departs d ON v.num_vol = d.num_vol WHERE id_departs = %s",[depart])
            query = cur.fetchall()[0]
            ts_depart,ts_arrivee = query
            print(ts_depart,ts_arrivee)
            ts_vol = (ts_arrivee-ts_depart).seconds//3600
            print(ts_vol)
            cur.execute("SELECT pilote_1,pilote_2,equipage_1,equipage_2 FROM departs WHERE id_departs = %s",[depart])
            query = cur.fetchall()[0]
            employes_list = [x for x in query]
            print(query)
            print(employes_list)
            for navigant in employes_list :
                query = "UPDATE naviguants SET nbr_heures_vol = nbr_heures_vol - %s WHERE numero_securite_sociale = %s"
                cur.execute(query, (ts_vol,navigant))
                mysql.connection.commit()

        # Supprimer les départs
        query= 'DELETE FROM departs WHERE id_departs IN (%s)' % format_strings
        cur.execute(query, tuple(deletion_departs_list))
        mysql.connection.commit()

        # Afficher en message flash les suppressions de départs et de billets
        for x in billets:
            flash('Le billet {} associé au départ {} a été supprimé.'.format(x[0],x[1]),"alert alert-info")
        for x in deletion_departs_list:
            flash('Le départ {} a été supprimé.'.format(x),"alert alert-info")

    def function_deletion_vols(deletion_vols_list):
        format_strings = ','.join(['%s'] * len(deletion_vols_list))
        query= 'DELETE FROM vols WHERE num_vol IN (%s)' % format_strings
        cur.execute(query, tuple(deletion_vols_list))
        mysql.connection.commit()
        for vol in deletion_vols_list:
            flash('Le vol {} a été supprimé.'.format(vol),"alert alert-info")

    def function_deletion_employes(deletion_employes_list):
        # Supprimer les instances de l'employé dans la table navigant
        for z in deletion_employes_list:
            query = 'SELECT * FROM naviguants WHERE numero_securite_sociale = %s'
            cur.execute(query, [z])
            if [x[0] for x in cur.fetchall()] == []:
                pass
            else: # Delete from navigant
                query= 'DELETE FROM naviguants WHERE numero_securite_sociale = %s'
                cur.execute(query, [z])
                mysql.connection.commit()

        # Supprimer les instances de l'employé dans la table employé
        print(deletion_employes_list)
        format_strings = ','.join(['%s'] * len(deletion_employes_list))
        print()
        query= 'DELETE FROM employes WHERE numero_securite_sociale IN (%s)' % format_strings
        cur.execute(query, tuple(deletion_employes_list))
        mysql.connection.commit()
        for employe in deletion_employes_list:
            flash('L\'employée {} a été supprimé.'.format(employe),"alert alert-info")

    # SUPPRIMER BILLET
    if deletion_billets!=[]:
        function_deletion_billets(deletion_billets)

    # SUPPRIMER PASSAGER
    if deletion_passagers!=[]:
        function_deletion_passagers(deletion_passagers)

    # SUPPRIMER DEPART
    if deletion_departs!=[]:
        function_deletion_departs(deletion_departs)

    # Retirer tous les vols présents dans la table départs
    if deletion_vols!=[]:
        print('-----',deletion_vols)
        deletion_vols_copy = [x for x in deletion_vols]
        for z in deletion_vols_copy:
            print(z)
            query = 'SELECT * FROM departs WHERE num_vol = %s'
            cur.execute(query, [z])
            tuple_departs=cur.fetchall()
            print('+++++',tuple_departs)
            if tuple_departs == ():
                pass
            else :
                deletion_vols.remove(z)
                for depart in tuple_departs:
                    flash('Le vol {} est associé au départ numéro {}. Veuillez supprimer ce départ. Attention, la suppression d\'un départ entraîne la suppression des billets associés'.format(z,depart[-1]),"alert alert-danger")

    # SUPPRIMER VOL
    if deletion_vols!=[]:
        function_deletion_vols(deletion_vols)

    # Retirer tous les employés présents dans la table départs
    if deletion_employes!=[]:
        # Trouver les départs concernés par les employés supprimés
        # Retirer de la liste de suppression les employés concernés par un départ
        for z in deletion_employes:
            query = 'SELECT * FROM departs WHERE %s in (pilote_1,pilote_2,equipage_1,equipage_2)'
            cur.execute(query, [z])
            tuple_departs=cur.fetchall()
            if tuple_departs == ():
                pass
            else: # Afficher avec Flash les employés apparaissant dans le départ
                deletion_employes.remove(z)
                query = 'SELECT nom,prenom FROM employes WHERE numero_securite_sociale = %s'
                cur.execute(query, [z])
                prenom_flash,nom_flash=cur.fetchall()[0]
                for depart in tuple_departs:
                    depart_flash=depart[0]
                    flash('{} {} apparaît dans le départ associé au numéro de vol {}. Veuillez supprimer ce départ.'.format(prenom_flash,nom_flash,depart_flash),"alert alert-danger")

    # SUPPRIMER EMPLOYÉ
    if deletion_employes!=[]:
        function_deletion_employes(deletion_employes)
    return('')

@app.route('/creer/employe', methods=['GET', 'POST'])
def creer_employe():
    form = EmployeeCreationForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        numero_securite_sociale = form.numero_securite_sociale.data
        cur.execute("SELECT numero_securite_sociale FROM employes")
        data = [x[0] for x in cur.fetchall()]
        if numero_securite_sociale in data:
            flash('Le numéro de sécurité sociale {} existe déjà dans la base'.format(numero_securite_sociale),"alert alert-danger")
        else :
            nom = form.nom.data
            prenom = form.prenom.data
            adresse = form.adresse.data
            ville = form.ville.data
            pays = form.pays.data
            salaire = form.salaire.data
            type = form.type.data
            flash('{} {} est désormais un employé.'.format(prenom,nom),"alert alert-info")
            cur.execute("INSERT INTO employes(numero_securite_sociale,nom,prenom,adresse,ville,pays,salaire,type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(numero_securite_sociale,nom,prenom,adresse,ville,pays,salaire,type))
            mysql.connection.commit()
            cur.close()
            if type == 'naviguant':
                return redirect(url_for('creer_employe_navigant',numero_securite_sociale = numero_securite_sociale))
            else:
                return redirect('/accueil')
    return render_template('creer_employe.html', title='Air Centrale - Créer employé', form=form)

@app.route('/creer/employe/navigant/<numero_securite_sociale>', methods=['GET', 'POST'])
def creer_employe_navigant(numero_securite_sociale):
    form = NaviguantCreationForm()
    choices_fonction=[('',' - '),('pilote','Pilote'),('steward','Steward'),('hôtesse','Hôtesse')]
    form.fonction.choices=choices_fonction
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        nbr_heures_vol = 0
        fonction = form.fonction.data
        num_licence_pilote = form.num_licence_pilote.data
        cur.execute("SELECT num_licence_pilote FROM naviguants")
        data = [x[0] for x in cur.fetchall()]
        if fonction == 'pilote' and num_licence_pilote == None:
            flash('Un pilote doit avoir un numéro de license',"alert alert-danger")
        else :
            if fonction == 'pilote' and num_licence_pilote in data:
                flash('Le numéro de licence pilote {} existe déjà dans la base'.format(num_licence_pilote),"alert alert-danger")
            else:
                if fonction == 'pilote':
                    cur.execute("INSERT INTO naviguants(numero_securite_sociale,nbr_heures_vol,fonction,num_licence_pilote) VALUES (%s, %s, %s, %s)",(numero_securite_sociale,nbr_heures_vol,fonction,num_licence_pilote))
                else :
                    cur.execute("INSERT INTO naviguants(numero_securite_sociale,nbr_heures_vol,fonction,num_licence_pilote) VALUES (%s, %s, %s, %s)",(numero_securite_sociale,nbr_heures_vol,fonction,None))
                mysql.connection.commit()
                flash('L\'employé naviguant {} a été créé.'.format(numero_securite_sociale),"alert alert-info")
                cur.close()
                return redirect('/accueil')
    return render_template('creer_employe_navigant.html', title='Air Centrale - Créer employé naviguant', form=form)

@app.route('/creer/vol', methods=['GET', 'POST'])
def creer_vol():
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
            flash('Le numéro de vol {} existe déjà dans la base, veuillez le changer.'.format(num_vol),"alert alert-danger")
        else:
            id_liaison = form.id_liaison.data
            ts_annee_depart = int(form.ts_annee_depart.data)
            ts_mois_depart = int(form.ts_mois_depart.data)
            ts_jour_depart = int(form.ts_jour_depart.data)
            ts_heure_depart = int(form.ts_heure_depart.data)
            ts_minute_depart = int(form.ts_minute_depart.data)
            ts_heures = form.ts_vol_heures.data
            ts_minutes = form.ts_vol_minutes.data
            if ts_heures == '':
                ts_heures = 0
            if ts_minutes == '':
                ts_minutes = 0
            ts_vol = int(ts_heures)*3600 + int(ts_minutes)*60
            if ts_vol == 0:
                flash('Le temps de vol ne peut pas être nul.',"alert alert-danger")
                cur.close()
            else:
                ts_depart=datetime.datetime(ts_annee_depart,ts_mois_depart,ts_jour_depart,ts_heure_depart,ts_minute_depart,0)
                ts_arrivee = int(ts_depart.strftime('%s')) + ts_vol
                ts_arrivee=datetime.datetime.fromtimestamp(ts_arrivee)
                cur.execute("INSERT INTO vols(num_vol,ts_depart,ts_arrivee,liaison) VALUES (%s, %s, %s, %s)",(num_vol,ts_depart,ts_arrivee,id_liaison))
                mysql.connection.commit()
                flash('Le vol numéro {} vient d\'être créé.'.format(num_vol),"alert alert-info")
                cur.close()
                return redirect('/accueil')
    return render_template('creer_vol.html', title='Air Centrale - Créer vol', form=form)

@app.route('/creer/depart', methods=['GET', 'POST'])
def creer_depart():
    cur = mysql.connection.cursor()
    form = DepartCreationForm()
    cur.execute("SELECT num_vol,ts_depart,ts_arrivee,liaison FROM vols v WHERE (v.num_vol NOT IN (SELECT d.num_vol FROM departs d) AND ts_depart>NOW())")
    vols=cur.fetchall()
    print('vols :',vols)
    vols_display = []
    for vol in vols:
        cur.execute("SELECT a1.code ,a1.pays , a2.code, a2.pays FROM liaisons l JOIN aeroports a1 ON l.aeroport_origine = a1.id_aeroports JOIN aeroports a2 ON l.aeroport_destination = a2.id_aeroports WHERE l.id_liaison = %s",[vol[3]])
        liaison = cur.fetchall()[0]
        liaison_display = ' - '.join((liaison[0],liaison[2]))
        vols_display.append({'num_vol':vol[0],'ville_depart':liaison[1],'ts_depart':vol[1],'ville_arrivee':liaison[3],'ts_arrivee':vol[2],'liaison':liaison_display})
    if form.validate_on_submit():
        selected_vol = request.form.getlist('selection')
        if selected_vol != []:
            selected_vol=selected_vol[0]
            return redirect(url_for('creer_depart_conditions',selected_vol = selected_vol,aeroport_depart=liaison[0],aeroport_arrivee=liaison[2]))
        else:
            pass
    return render_template('creer_depart.html', title='Air Centrale - Créer départ', vols=vols_display, form=form)

# creer_depart_conditions() - Incrémenter le nombre d'heures de vol d'un pilote
@app.route('/creer/depart/conditions/<selected_vol>_<aeroport_depart>-<aeroport_arrivee>', methods=['GET', 'POST'])
def creer_depart_conditions(selected_vol,aeroport_depart,aeroport_arrivee):
    cur = mysql.connection.cursor()
    form = DepartConditionsCreationForm()
    # Find the country to be in as well as the time for the departure
    cur.execute("SELECT a.pays,v.ts_depart,v.ts_arrivee FROM vols v JOIN liaisons l ON v.liaison = l.id_liaison JOIN aeroports a ON l.aeroport_origine = a.id_aeroports WHERE v.num_vol = %s",[selected_vol])
    pays_depart,ts_depart,ts_arrivee = cur.fetchall()[0]
    print('ts_depart :',ts_depart)
    print('ts_arrivee :',ts_arrivee)
    nbr_heures_vol = (int(ts_arrivee.strftime('%s')) - int(ts_depart.strftime('%s')))//3600

    tps_vol = ts_arrivee - ts_depart

    ts_depart_days = ts_depart.strftime("%Y-%m-%d")
    ts_depart_days = ts_depart_days.split('-')
    ts_arrivee_days = ts_arrivee.strftime("%Y-%m-%d")
    ts_arrivee_days = ts_arrivee_days.split('-')
    ts_vol_days = (datetime.datetime(int(ts_arrivee_days[0]),int(ts_arrivee_days[1]),int(ts_arrivee_days[2]))-datetime.datetime(int(ts_depart_days[0]),int(ts_depart_days[1]),int(ts_depart_days[2]))).days
    if ts_vol_days!=0:
        tps_vol = str(ts_vol_days)+' '+str(tps_vol)
    else :
        tps_vol = tps_vol
    print('tps_vol :',tps_vol)
    print('nbr_heures_vol :',nbr_heures_vol)
    print('aeroport_depart :',aeroport_depart)
    print('aeroport_arrivee :',aeroport_arrivee)
    query = executeScriptsFromFile(os.path.abspath(os.path.dirname(__file__))+'/requete_depart_conditions.sql',ts_depart,ts_arrivee,tps_vol,nbr_heures_vol,aeroport_depart,aeroport_arrivee)
    pilotes_disponibles=[]
    membres_disponibles=[]
    for employe in query :
        nom_employe = employe[0]
        prenom_employe = employe[1]
        fonction_employe = employe[2]
        numero_securite_sociale = employe[3]
        if fonction_employe =='pilote':
            pilotes_disponibles.append({'numero_securite_sociale':numero_securite_sociale,'nom':nom_employe,'prenom':prenom_employe,'fonction':fonction_employe})
        else:
            membres_disponibles.append({'numero_securite_sociale':numero_securite_sociale,'nom':nom_employe,'prenom':prenom_employe,'fonction':fonction_employe})
    query = executeScriptsFromFile(os.path.abspath(os.path.dirname(__file__))+'/requete_appareils_disponibles.sql',ts_depart,ts_arrivee,tps_vol,nbr_heures_vol,aeroport_depart,aeroport_arrivee)
    print(query)
    data = [x[0] for x in query]
    print(data)
    choices_immatriculation_appareil=[('',' - ')]+[(x,x) for x in data]
    form.immatriculation_appareil.choices=choices_immatriculation_appareil
    if form.validate_on_submit():
        pilotes = request.form.getlist('pilotes')
        nbr_pilotes = len(pilotes)
        membres = request.form.getlist('membres')
        nbr_membres = len(membres)
        print('pilotes :',pilotes)
        print('membres :',membres)
        immatriculation_appareil = form.immatriculation_appareil.data
        flash('Un nouveau départ vient d\'être associé au vol numéro {}'.format(selected_vol),"alert alert-info")
        for x in pilotes + membres :
            cur.execute("UPDATE naviguants SET nbr_heures_vol = nbr_heures_vol + %s WHERE numero_securite_sociale = %s",[int(nbr_heures_vol),x])
            mysql.connection.commit()
        while len(pilotes) < 2:
            pilotes.append(None)
        while len(membres) < 2:
            membres.append(None)
        print('pilotes :',pilotes)
        print('membres :',membres)
        cur.execute("INSERT INTO departs(num_vol,pilote_1,pilote_2,equipage_1,equipage_2,nbr_places_libres,immatriculation) VALUES (%s, %s, %s, %s, %s, %s, %s)",(selected_vol,pilotes[0],pilotes[1],membres[0],membres[1],100,immatriculation_appareil))
        mysql.connection.commit()
        return redirect('/accueil')
    return render_template('creer_depart_conditions.html', title='Air Centrale - Créer départ conditions', form = form, pilotes_disponibles = pilotes_disponibles,membres_disponibles = membres_disponibles)

@app.route('/visualiser/personnel', methods=['GET', 'POST'])
def visualiser_personnel():
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
    return render_template('visualiser_personnel.html', title='Air Centrale - Visualiser personnel',employes=employes_display,vol_en_cours=vol_en_cours,departs_prevus=prevus_display,departs_passes=passes_display)

@app.route('/reserver/billet', methods=['GET', 'POST'])
def reserver_billet():
    cur = mysql.connection.cursor()
    form = BilletReservationForm()
    cur.execute("SELECT d.id_departs,v.ts_depart,v.ts_arrivee,v.liaison,d.nbr_places_libres FROM vols v JOIN departs d ON v.num_vol = d.num_vol WHERE (d.nbr_places_libres > 0 and v.ts_depart > NOW())")
    departs=cur.fetchall()
    departs_display = []
    for depart in departs:
        cur.execute("SELECT a1.code ,a1.pays , a2.code, a2.pays FROM liaisons l JOIN aeroports a1 ON l.aeroport_origine = a1.id_aeroports JOIN aeroports a2 ON l.aeroport_destination = a2.id_aeroports WHERE l.id_liaison = %s",[depart[3]])
        liaison = cur.fetchall()[0]
        liaison_display = ' - '.join((liaison[0],liaison[2]))
        departs_display.append({'id_depart':depart[0],'ville_depart':liaison[1],'ts_depart':depart[1],'ville_arrivee':liaison[3],'ts_arrivee':depart[2],'liaison':liaison_display,'places_libres':depart[4]})
    if form.validate_on_submit():
        selected_depart = request.form.getlist('selection')[0]
        return redirect(url_for('reserver_billet_passager',selected_depart = selected_depart))
    return render_template('reserver_billet.html', title='Air Centrale - Reserver billet',form=form,departs=departs_display)

@app.route('/reserver/billet/passager/<selected_depart>', methods=['GET', 'POST'])
def reserver_billet_passager(selected_depart):
    cur = mysql.connection.cursor()
    form = BilletConditionsReservationForm()
    # Générer les informations d'information du départ choisi
    cur.execute("SELECT d.id_departs,v.ts_depart,v.ts_arrivee,v.liaison FROM departs d JOIN vols v ON d.num_vol = v.num_vol WHERE d.id_departs = %s",[selected_depart])
    depart = cur.fetchall()[0]
    cur.execute("SELECT a1.code ,a1.pays , a2.code, a2.pays FROM liaisons l JOIN aeroports a1 ON l.aeroport_origine = a1.id_aeroports JOIN aeroports a2 ON l.aeroport_destination = a2.id_aeroports WHERE l.id_liaison = %s",[depart[3]])
    liaison = cur.fetchall()[0]
    liaison_display = ' - '.join((liaison[0],liaison[2]))
    travel_information = {'id_depart':depart[0],'ville_depart':liaison[1],'ts_depart':depart[1],'ville_arrivee':liaison[3],'ts_arrivee':depart[2],'liaison':liaison_display}
    # Si l'utilisateur valide le formulaire :
    if form.validate_on_submit():
        nom = form.nom.data.title()
        prenom = form.prenom.data.title()
        adresse = form.adresse.data
        ville = form.ville.data
        pays = form.pays.data
        cur.execute("SELECT * FROM passagers WHERE ( nom = %s AND prenom = %s)",(nom,prenom))
        passagers = cur.fetchall()
        # Ajouter le passager si il n'existe pas dans la base
        if passagers == ():
            cur.execute("INSERT INTO passagers(nom,prenom,adresse,ville,pays) VALUES (%s, %s, %s, %s, %s)",(nom,prenom,adresse,ville,pays))
            mysql.connection.commit()
            flash('{} {} a été ajouté à la base de données comme passager.'.format(prenom,nom),"alert alert-info")
        else : # Si le passager existe déjà dans la base, ne rien faire
            pass
        # Générer un nouveau nom de billet aléatoirement en vérifiant qu'il n'existe pas déjà
        cur.execute("SELECT num_billet FROM billets")
        num_billets_existants = [x[0] for x in cur.fetchall()]
        num_billet = random.randint(10000000, 99999999)
        while num_billet in num_billets_existants :
            num_billet = random.randint(10000000, 99999999)
        # Générer le temps d'émission du billet
        ts_emission = datetime.datetime.now()
        # Générer le numéro de départ du billet
        num_depart = selected_depart
        # Obtenir le numéro du passager (nécessite le commit dans "if passagers == ()")
        cur.execute("SELECT id_passager FROM passagers WHERE (nom = %s AND prenom = %s)",(nom,prenom))
        num_passager = cur.fetchall()[0][0]
        # Insérer le nouveau billet
        cur.execute("INSERT INTO billets(num_billet,ts_emission,num_depart,num_passager) VALUES (%s, %s, %s, %s)",(int(num_billet),ts_emission,int(num_depart),int(num_passager)))
        mysql.connection.commit()
        # Soustraire 1 du nombre de places disponibles du départ correspondant dans la table départs
        cur.execute("UPDATE departs SET nbr_places_libres = nbr_places_libres - 1 WHERE id_departs = %s",[num_depart])
        mysql.connection.commit()
        flash('Le billet {} appartenant à {} {} a été enregistré.'.format(num_billet,prenom,nom),"alert alert-info")
        return redirect(url_for('accueil'))
    return render_template('reserver_billet_passager.html', title='Air Centrale - Reserver billet',form=form,depart=travel_information)
