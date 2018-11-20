import os

class Config(object):

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    #Configure DB
    MYSQL_HOST = ''
    MYSQL_USER = ''
    MYSQL_PASSWORD = ''
    MYSQL_DB = ''
