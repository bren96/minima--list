from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from .forms import SignupForm, LoginForm
from .models import db, User, Todo
from flask import current_app as app
from datetime import datetime

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup Form."""
    signup_form = SignupForm()
    if request.method == 'POST':
        new_user = User(
            user = request.form['email'],
            password = request.form['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')

        #if signup_form.validate():
        #    flash('Logged in successfully.')
        #    return render_template('/index.html')
    return render_template('signup.html', form=signup_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form."""
    login_form = LoginForm()
    if request.method == 'POST':
        return '<h1>' + request.form['email'] + request.form['password'] + '</h1>'
    return render_template('login.html', form=login_form)

@app.route('/dashboard', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)
