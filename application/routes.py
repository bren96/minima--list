from flask import redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import SigninForm, SignupForm, task_checkbox
from .models import db, User, Todo
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@app.route('/')
def base():
    return redirect('/signin')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup Form."""
    signup_form = SignupForm()
    if request.method == 'POST':
        new_user = User(
            username = request.form['email'],
            password = request.form['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect('/signin')
        #if signup_form.validate():
        #    flash('Logged in successfully.')
        #    return render_template('/index.html')
    return render_template('signup.html', form=signup_form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """Login Form."""
    login_form = SigninForm()
    if request.method == 'POST':
        user = User.query.filter(User.username == request.form['email']).first()
        if user.password == request.form['password']:
            login_user(user)
            return redirect('/dashboard')
    return render_template('signin.html', form=login_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/signin')

@app.route('/dashboard', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content, username=current_user.username)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/dashboard')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.filter(Todo.username == current_user.username).all()
        task_form = task_checkbox()
        return render_template('index.html', tasks=tasks, form=task_form)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/dashboard')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/dashboard')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

@app.route('/check/<int:id>', methods=['GET', 'POST'])
@login_required
def check(id):
    task = Todo.query.get_or_404(id)
    if task.check == 0:
        task.check = 1
    else:
        task.check = 0
    try:
        db.session.commit()
    except:
        return 'There was an issue updating your task'
    return redirect('/dashboard')

@app.route('/update_notebook', methods=['GET', 'POST'])
@login_required
def update_notebook():
    tasks = Todo.query.filter(Todo.username == current_user.username).all()
    if request.method == 'POST':
        for task in tasks:
            if task.check == 1:
                db.session.delete(task)
                db.session.commit()
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')

@app.route('/user')
@login_required
def home():
    return 'The Current User is ' + current_user.username
