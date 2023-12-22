from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///expensesDB.db'
app.config['SECRET_KEY'] ='key11553124134'

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

from application import routes 