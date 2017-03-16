import os
from flask import Flask, render_template, redirect, session, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
#from models import Base, Issue, User


app = Flask(__name__)

#Base.metadata.create_all(engine)
#DBSession =  sessionmaker(bind=engine)
#sessions = DBSession()

@app.route('/index')
def index():

    return render_template('home.html')

@app.route('/issue/')
def issue():
        return render_template('newissue.html')

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/register/')
def register():
    return render_template('signup.html')

@app.route('/viewissue/')
def viewissue():
    return render_template('Viewissue.html')


if __name__ == '__main__':
    app.secret_key = "secret_key"
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)




