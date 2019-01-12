# app-airline_management - Airline Management Application

## Python Requirements

Python 3 is used for this application.

## Flask Requirements

The following modules need to be installed in order to run the flask application.
```
$ pip3 install flask
$ pip3 install flask-mysqldb
$ pip3 install flask-wtf
$ pip3 install flask-bootstrap
```

## Flask Server

In order to launch the flask application, move to the application directory, then enter the following lines in the command line.

```
$ set FLASK_APP=application_gca.py
$ flask run
```

## Heroku Update MySQL Database

Go to the git folder, then type :
```
heroku config
```
Then fill the following line

```
mysql --host=xxxx --user=xxxx --password=xxxx --reconnect heroku_xxxx < schema.sql
```

## References

Flask Application Tutorial - https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

