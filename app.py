from Tool import app, db
import os
from Tool.forms import RegistrationForm, LoginForm , ProjectForm , TaskForm , QueryForm
from Tool.models import User , Project , Task
from flask import render_template,request, url_for, redirect, flash ,abort
from flask_login import current_user, login_required, login_user , logout_user
from picture_handler import add_profile_pic
from sqlalchemy import desc, asc
from werkzeug.utils import secure_filename
from flask import send_from_directory

ALLOWED_EXTENSIONS = {'csv'}

@app.route('/' , methods = ['GET' , 'POST'])
def index():
    return render_template("index.htm")

@app.route('/register' , methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(name = form.name.data,
                    username = form.username.data,
                    email = form.email.data ,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        if form.picture.data is not None:
            id = user.id
            pic = add_profile_pic(form.picture.data,id)
            user.profile_image = pic
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.htm', form = form)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/login' , methods = ['GET' , 'POST'])
def login():
    form = LoginForm()
    error = ''
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data) :

            login_user(user)
            flash('Log in Success!')

            next = request.args.get('next')
            if next == None or not next[0] =='/':
                next = url_for('index')
            return redirect(next)
        elif user is not None and user.check_password(form.password.data) == False:
            error = 'Wrong Password'
        elif user is None:
            error = 'No such login Pls create one'
    return render_template('login.htm', form=form, error = error)

@app.route('/makeproject' , methods = ['GET' , 'POST'])
@login_required
def makeproject():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name = form.name.data,
                        description = form.description.data,
                        userid = current_user.id)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('projects'))
    return render_template('makeproject.htm' , form = form)

@app.route('/projects' , methods = ['GET' , 'POST'])
@login_required
def projects():
    projects = Project.query.filter_by(userid = current_user.id)
    return render_template('projects.htm' , projects = projects)

@app.route('/maketask/<projectid>' , methods = ['GET' , 'POST'])
@login_required
def maketask(projectid):
    project = Project.query.get_or_404(projectid)
    if current_user != project.user:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(name = form.name.data,
                    description = form.description.data,
                    projectid = projectid)
        project.completed = 'No'
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks' , projectid = projectid))
    return render_template('maketask.htm' , form = form)

@app.route('/tasks/<projectid>' , methods = ['GET' , 'POST'])
@login_required
def tasks(projectid):
    tasks = Task.query.filter_by(projectid = projectid)
    na = 'No'
    nas = 'NO'
    return render_template('tasks.htm' , tasks = tasks , projectid = projectid , na = na ,nas = nas)

@app.route('/task/<task_id>' , methods = ['GET' , 'POST'])
@login_required
def task(task_id):
    task = Task.query.get(task_id)
    print(task_id)
    if task.completed == 'No':
        Status = 'Not Completed'
    else:
        Status = 'Completed'
    return render_template('task.htm' , task = task , Status = Status)


@app.route('/change/<to>/<task_id>' , methods = ['GET' , 'POST'])
@login_required
def change(to , task_id):
    a = 1
    task = Task.query.get_or_404(task_id)
    project = Project.query.get(task.projectid)
    task.completed = to
    db.session.commit()
    for t in project.tasks:
        if t.completed == 'No':
            a = 2
            break
    print(a)
    if a == 2:
        project.completed = 'No'
        db.session.commit()
    else:
        project.completed = 'Yes'
        db.session.commit()
    return redirect(url_for('tasks' , projectid = project.id))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/queryform', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save('Tool/static/csvs/data.csv')
            return redirect(url_for('uploaded_file'))
    return render_template('query.htm')

@app.route('/uploads')
def uploaded_file():
    return send_from_directory('Tool/static/csvs' , 'data.csv')

if __name__ == '__main__':
    app.run(debug = True)
