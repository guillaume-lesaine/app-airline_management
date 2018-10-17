from flask import render_template
from app import app
from app.forms import AirportCreationForm
from flask_mysqldb import MySQL

mysql=MySQL(app)


@app.route('/')
@app.route('/index')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Stock")
    data = cur.fetchone()
    cur.close()
    print(data)
    return render_template('index.html', title='Home')

@app.route('/creation/airport', methods=['GET', 'POST'])
def creation_airport():
    form = AirportCreationForm()
    if form.validate_on_submit():
        name = form.name.data
        code = form.code.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Stock(idStock,idIngredient,quantite) VALUES(%s, %s, %s)",(10,name,code))
        mysql.connection.commit()
        cur.close()
        return redirect('/index')
    return render_template('creation_airport.html', title='Création aéroport', form=form)
