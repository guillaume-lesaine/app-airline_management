from flask import render_template, flash, redirect
from app import app
from app.forms import AirportCreationForm, EmployeeCreationForm, NaviguantCreationForm
from flask_mysqldb import MySQL

mysql=MySQL(app)


@app.route('/')
@app.route('/index')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM aeroports")
    #cur.execute("SELECT * FROM Stock")
    data = cur.fetchall()
    cur.close()
    print(data)
    return render_template('index.html', title='Home')

@app.route('/creation/airport', methods=['GET', 'POST'])
def creation_airport():
    form = AirportCreationForm()
    if form.validate_on_submit():
        code = form.code.data
        nom = form.nom.data
        cur = mysql.connection.cursor()
        print(nom)
        print(code)
        #cur.execute("SELECT * FROM aeroports")
        cur.execute("INSERT INTO aeroports(id_aeroports,code,nom) VALUES (DEFAULT, %s, %s)",(code,nom))
        mysql.connection.commit()
        cur.close()
        return redirect('/index')
    return render_template('creation_airport.html', title='Création aéroport', form=form)

@app.route('/creation/employee', methods=['GET', 'POST'])
def creation_employee():
    form = EmployeeCreationForm()
    if form.validate_on_submit():
        numero_securite_sociale = form.numero_securite_sociale.data
        cur = mysql.connection.cursor()
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
                return redirect('/creation/employee/naviguant')
            else:
                return redirect('/index')
    return render_template('creation_employee.html', title='Création employé', form=form)

@app.route('/creation/employee/naviguant', methods=['GET', 'POST'])
def creation_employee_naviguant():
    form = NaviguantCreationForm()
    if form.validate_on_submit():
        nbr_heures_vol = form.nbr_heures_vol.data
        print(nbr_heures_vol)
        fonction = form.fonction.data[0]
        print(fonction)
        num_license_pilote = form.num_license_pilote.data
        print(num_license_pilote)
        if fonction == 'pilote' and num_license_pilote == None:
            flash('Un pilote doit avoir un numéro de license')
        else :
            flash('Un employé naviguant a été créé.')
            #cur.execute("INSERT INTO employes(numero_securite_sociale,nom,prenom,adresse,ville,pays,salaire,type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(numero_securite_sociale,nom,prenom,adresse,ville,pays,salaire,type))
            #mysql.connection.commit()
            #cur.close()
            return redirect('/index')
    return render_template('creation_employee_naviguant.html', title='Création employé naviguant', form=form)
