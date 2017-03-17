import os
from flask import Flask, render_template, redirect, session, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from models import Base, Issue, User,engine
from authform import LoginForm,RegistrationForm
from flask_login import login_required,login_user, logout_user, current_user
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)


Base.metadata.create_all(engine)
DBSession =  sessionmaker(bind=engine)
sessions = DBSession()


@app.route('/')
def index():
        return render_template('home.html')


@app.route('/admin/')
def admin():
    return render_template('adminviews.html')


@app.route('/login/', methods=['GET', 'POST'])
def sign_in():
    """Login functionality"""

    form = LoginForm()
    if form.validate_on_submit():
        user = sessions.query(User).filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')

    return render_template('login.html', form=form, title='Login')

    
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                            username=form.username.data,
                            f_name=form.first_name.data,
                            l_name=form.last_name.data,
                            password=form.password.data)
        sessions.add(user)
        sessions.commit()
        flash('You have been registered successfully.')
        return redirect(url_for('sign_in'))

    return render_template('register.html', form=form, title='Register')


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
        edit_issue = update(Issues).where(id==int(id)).values(name=title, remarks=comment)
        sessions.execute(edit_issue)
        sessions.commit()
        flash(u'Issue is updated!', "success")


    return redirect(url_for("admin_view_issues"))


if __name__ == '__main__':
    app.secret_key = "secret_key"
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)

