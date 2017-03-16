import os
from flask import Flask, render_template, redirect, session, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from models import Base, Issue, User

app = Flask(__name__)
app.secret_key = ""

Base.metadata.create_all(engine)
DBSession =  sessionmaker(bind=engine)
sessions = DBSession()


@app.route('/index')
def index():
        return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    """Login functionality"""

    if request.method == 'POST':
        user = sessions.query(Users).filter_by(username =request.form['username'], password=request.form['password']).one()
        flash(u'You are logged in', "success" )
        session['Username'] = request.form['username']
        session['user_type'] = request.form['username']
        session['id'] = user.id
        session['logged'] = True
        if user.user_type == 'admin':
            return redirect(url_for(''))
        else:
            return redirect(url_for(''))
            return render_template("signup.html")


@app.route('/signup', methods=['GET', 'POST'] )
def sign_up():
    """User signs in """
    if request.method == 'POST':
    	user_type = request.form['user_type']
        f_name = request.form['first name']
        l_name = request.form['last name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        
        if role == 'admin':
            admin = sessions.query(User).filter_by(user_type = 'admin')
            if admin != None:
                flash(u'Sorry there is an admin!!', "error")
                return render_template("signup.html")
        newuser = Users(username=username, password=password, email=email)
        sessions.add(newuser)
        sessions.commit()
        flash(u'You are successfully signed up', "success")
        return redirect(url_for('sign_in'))
    return render_template("signup.html")


@app.route('/signin/newissue', methods=['GET', 'POST'] )
def new_issue():
    """lets user post issues"""
    if 'Username' in session:
        username = session['Username'] 
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            priority = request.form['priority']
            department = request.form['department']
            newissue = Issues(title=title, description=description, priority=priority, department=department, user_id = session['id'] )
            sessions.add(newissue)
            sessions.commit()
            flash(u'You issue has been raised!', "success")
            return redirect(url_for(''))
        else:
            return render_template("newissue.html", user=username)
    else:
        return redirect(url_for('profile'))


app.route('/user/viewissues')
def user_view_issues():
    """function lets users view issues"""
    results = sessions.query(Issues).filter_by(user_id = session['id']).all()
    return render_template("allissues.html", results=results)

@app.route('/admin/viewissues')
def admin_view_issues():
    """Admin view issues"""
    issues = sessions.query(Issues).filter_by(department= session['department']).all()
    users = sessions.query(Users).all()
    return render_template("viewissues.html", results=issues, users = users)

@app.route('/signout')
def sign_out():
    """signout functionality here"""
    session.clear()
    return redirect(url_for('home'))


@app.route('/admin/update', methods=['POST'])
def update_issue():
    """This function implements update issues"""
    if request.method == 'POST':
        id = request.form['issue_id']
        title = request.form['title']
        status = request.form['status']
        comment = request.form['comment']
        edit_issue = update(Issues).where(id==int(id)).values(name=title, resolved=status, remarks=comment)
        sessions.execute(edit_issue)
        sessions.commit()
        flash(u'Issue is updated!', "success")


    return redirect(url_for("admin_view_issues"))


if __name__ == '__main__':
    app.secret_key = "secret_key"
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)







