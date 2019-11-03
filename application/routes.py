from flask import redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import SigninForm, SignupForm, taskForm, notebookForm
from .models import db, User, Todo, Notebooks
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
            return redirect('/notebooks')
    return render_template('signin.html', form=login_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/signin')

@app.route('/notebooks', methods=['POST', 'GET'])
@login_required
def notebook():
    if request.method == 'POST':
        notebook_name = request.form['content']
        new_notebook = Notebooks(notebook=notebook_name, username=current_user.username)
        try:
            db.session.add(new_notebook)
            db.session.commit()
            return redirect('/notebooks')
        except:
            return "There was an issue adding your notebook"

    else:
        notebooks = Notebooks.query.filter(Notebooks.username == current_user.username)
        return render_template('notebooks.html', notebooks=notebooks)

@app.route('/dashboard/<int:id>', methods=['POST', 'GET'])
@login_required
def index(id):
    notebook = Notebooks.query.get_or_404(id)
    if notebook.username == current_user.username:
        notebook_name = notebook.notebook
        if request.method == 'POST':
            task_content = request.form['content']
            new_task = Todo(
                content=task_content,
                username=current_user.username,
                notebook=notebook_name,
                completed=0)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/dashboard/' + str(id))
            except:
                return 'There was an issue adding your task'
        else:
            tasks = Todo.query.filter(
                Todo.username == current_user.username,
                Todo.notebook == notebook_name,
                Todo.completed == False).order_by(Todo.date_created).all()
            task_form = taskForm()
            return render_template('index.html', tasks=tasks, form=task_form, notebook=notebook)
    else:
        'Hmmm...This isnt your notebook'

@app.route('/delete/<int:task_id>/<int:notebook_id>')
@login_required
def delete(task_id, notebook_id):
    if task_id == 0:
        notebook = Notebooks.query.get_or_404(notebook_id)
        notebooks_tasks = Todo.query.filter(Todo.notebook == notebook.notebook).all()
        try:
            for each in notebooks_tasks:
                db.session.delete(each)
            db.session.delete(notebook)
            db.session.commit()
            return redirect('/notebooks')
        except:
            return 'There was a problem deleting that notebook'
    else:
        task_to_delete = Todo.query.get_or_404(task_id)
        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/dashboard/' + str(notebook_id))
        except:
            return 'There was a problem deleting that task'

@app.route('/update/<int:task_id>/<int:notebook_id>', methods=['GET', 'POST'])
@login_required
def update(task_id, notebook_id):
    if task_id == 0:
        notebook = Notebooks.query.get_or_404(notebook_id)
        content = notebook.notebook
        if request.method == 'POST':
            notebook.notebook = request.form['content']
            tasks = Todo.query.filter(Todo.notebook == content).all()
            for each in tasks:
                each.notebook = notebook.notebook
                db.session.commit
            try:
                db.session.commit()
                return redirect('/notebooks')
            except:
                return "There was an issue updating your notebook"
        else:
            return render_template(
                'update.html',
                task=task_id,
                notebook=notebook,
                content=content
            )
    else:
        task = Todo.query.get_or_404(task_id)
        notebook = Notebooks.query.get_or_404(notebook_id)
        content = task.content
        if request.method == 'POST':
            task.content = request.form['content']
            try:
                db.session.commit()
                return redirect('/dashboard/' + str(notebook_id))
            except:
                return 'There was an issue updating your task'
        else:
            return render_template(
                'update.html',
                task=task_id,
                notebook=notebook,
                content=content
            )

@app.route('/check/<int:task_id>/<int:notebook_id>', methods=['GET', 'POST'])
@login_required
def check(task_id, notebook_id):
    task = Todo.query.get_or_404(task_id)
    if task.check == False:
        task.check = True
    else:
        task.check = False
    try:
        db.session.commit()
    except:
        return 'There was an issue updating your task'
    return redirect('/dashboard/' + str(notebook_id))

@app.route('/update_notebook/<int:notebook_id>', methods=['GET', 'POST'])
@login_required
def update_notebook(notebook_id):
    notebook = Notebooks.query.get_or_404(notebook_id)
    notebook_name = notebook.notebook
    tasks = Todo.query.filter(
        Todo.username == current_user.username,
        Todo.notebook == notebook_name,
        Todo.completed == False).all()
    if request.method == 'POST':
        for task in tasks:
            if task.check == True:
                task.completed = True
                db.session.commit()
        return redirect('/dashboard/' + str(notebook_id))
    else:
        return redirect('/dashboard/' + str(notebook_id))

@app.route('/user')
@login_required
def home():
    return 'The Current User is ' + current_user.username
