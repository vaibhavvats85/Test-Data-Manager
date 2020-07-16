from flask import Flask
from flask_mysqldb import MySQL
import yaml
import logging as logger
logger.basicConfig(level = 'DEBUG')

app = Flask(__name__)

#configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

if __name__=='__main__':
    logger.debug('starting the application')
    from api import *
    app.run()