from flask import Flask
from flask_mysqldb import MySQL
from projectDB.login import login
from projectDB.sign_up import sign_up


app = Flask(__name__)

## configuration of database

app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = 'wetmy0-robjyt-Gamqur'
app.config["MYSQL_DB"] = 'base'
app.config["MYSQL_HOST"] = 'localhost'
app.config["SECRET_KEY"] = 'key' 
app.config["WTF_CSRF_SECRET_KEY"] = 'key' 

## initialize database connection object
db = MySQL(app)


from projectDB import routes
from projectDB.login import routes
from projectDB.sign_up import routes
app.register_blueprint(login)
app.register_blueprint(sign_up)
