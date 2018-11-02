import os

class Config(object):

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Configure DB
    # MYSQL_HOST = 'localhost'
    # MYSQL_USER = 'root'
    # MYSQL_PASSWORD = 'L.Simon16011675'
    # MYSQL_DB = 'airline'

    MYSQL_HOST = 'us-cdbr-iron-east-01.cleardb.net'
    MYSQL_USER = 'bee711030d7cd2'
    MYSQL_PASSWORD = 'd47e8ba9'
    MYSQL_DB = 'heroku_03b85268317665c'
