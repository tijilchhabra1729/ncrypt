from Tool import app, db
import os
from Tool.forms import RegistrationForm, LoginForm, ProjectForm, TaskForm, QueryForm, QueryReq, UpdateTask, QueryReqWhere, UpdateQuery
from Tool.models import User, Project, Task
from flask import render_template, request, url_for, redirect, flash, abort
from flask_login import current_user, login_required, login_user, logout_user
from picture_handler import add_profile_pic
from sqlalchemy import desc, asc
from werkzeug.utils import secure_filename
from flask import send_from_directory
import csv

ALLOWED_EXTENSIONS = {'csv'}


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.htm")


@app.route('/querygen', methods=['GET', 'POST'])
@login_required
def querygen():
    return render_template("howto.htm")


@app.route('/create/select', methods=['GET', 'POST'])
@login_required
def dashboard():
    try:
        mystr = "SELECT "
        form = QueryReq()
        if form.validate_on_submit():
            table_name = form.table_name.data
        data = open('Tool/static/csvs/' + current_user.username +
                    '.csv', encoding='utf-8')
        csv_data = csv.reader(data)
        data_lines = list(csv_data)
        if request.method == 'POST':
            filter_list = request.form.getlist("filter_value")
            column_list = request.form.getlist("column_name")
            filter_list = [i for i in filter_list if i]
            for sublist in column_list:
                mylist = sublist.split(',')
                data = mylist[0]
                mydata = data[2:-1]
                mystr = mystr + mydata + ','
            mystr = mystr[:-1]
            mystr = mystr + " FROM " + table_name
            flash(mystr)
    except:
        return redirect(url_for('upload_file'))
    return render_template("dashboard.htm", data_lines=data_lines, form=form, mystr=mystr)


@app.route('/create/table', methods=['GET', 'POST'])
@login_required
def create_table():
    try:
        form = QueryReq()
        data = open('Tool/static/csvs/' + current_user.username +
                    'table_create' + '.csv', encoding='utf-8')
        csv_data = csv.reader(data)
        data_lines = list(csv_data)
        if form.validate_on_submit():
            table_name = form.table_name.data
            mystr = 'CREATE TABLE '
        if request.method == 'POST':
            primary_key = request.form.getlist("primary_key")
            line_one = mystr + table_name + ' ('
            myquery = [line_one]
            for v, d in data_lines:
                myquery.append('    ' + v + d + ',')
            myquery.append("PRIMARY_KEY" + " (" + primary_key[0] + ")")
            myquery.append(');')
            flash(myquery)
    except:
        return redirect(url_for('upload_file_create_table'))
    return render_template("table.htm", form=form, data_lines=data_lines)


@app.route('/create/where', methods=['GET', 'POST'])
@login_required
def create_where():
    try:
        value = ""
        mystr = "SELECT * FROM "
        myquery = []
        form = QueryReq()
        if form.validate_on_submit():
            table_name = form.table_name.data
            line_one = mystr + table_name
            myquery = [line_one]
        data = open('Tool/static/csvs/' + current_user.username +
                    'where' + '.csv', encoding='utf-8')
        csv_data = csv.reader(data)
        data_lines = list(csv_data)
        if request.method == 'POST':
            column_list = request.form.getlist("column_name")
            value_list_1 = request.form.getlist("value")
            value_list = []
            for i in value_list_1:
                if i:
                    value_list.append(i)
            line_two = "WHERE "
            for i in column_list:
                line_two = line_two + i + "=" + value_list.pop(0) + " AND "
            line_two = line_two[0:-4] + ";"
            myquery.append(line_two)
            flash(myquery)
            print(column_list)
            print(value_list)
    except:
        return redirect('upload_file_create_where')
    return render_template("where.htm", data_lines=data_lines, form=form, myquery=myquery)


@app.route('/create/update', methods=['GET', 'POST'])
@login_required
def update_query():
    form = UpdateQuery()
    if form.validate_on_submit():
        table_name = form.table_name.data
        column_name = form.column_name.data
        value = form.changed_val.data
        query = ["UPDATE " + table_name, "SET " + column_name + " = " + value]
        flash(query)
    return render_template("updatequery.htm", form=form)


@app.route('/edit_task/<projectid>', methods=['GET', 'POST'])
@login_required
def edit_task(projectid):
    tasks = Task.query.filter_by(projectid=projectid)
    na = 'No'
    nas = 'NO'
    taskss = []
    for task in tasks:
        taskss.append(task)
    taskss.reverse()
    return render_template("edit_task.htm", tasks=taskss, projectid=projectid, na=na, nas=nas)


@app.route('/edit_project', methods=['GET', 'POST'])
@login_required
def edit_project():
    projects = Project.query.filter_by(userid=current_user.id)
    projectss = []
    for project in projects:
        projectss.append(project)
    projectss.reverse()
    return render_template('edit_project.htm', projects=projectss)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(name=form.name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        if form.picture.data is not None:
            id = user.id
            pic = add_profile_pic(form.picture.data, id)
            user.profile_image = pic
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.htm', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):

            login_user(user)

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('projects')
            return redirect(next)
        elif user is not None and user.check_password(form.password.data) == False:
            error = 'Wrong Password'
        elif user is None:
            error = 'No such login Pls create one'
    return render_template('login.htm', form=form, error=error)


@app.route('/makeproject', methods=['GET', 'POST'])
@login_required
def makeproject():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data,
                          description=form.description.data,
                          userid=current_user.id)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('projects'))
    return render_template('makeproject.htm', form=form)


@app.route('/projects', methods=['GET', 'POST'])
@login_required
def projects():
    projects = Project.query.filter_by(userid=current_user.id)
    projectss = []
    for project in projects:
        projectss.append(project)
    projectss.reverse()
    return render_template('projects.htm', projects=projectss)


@app.route('/maketask/<projectid>', methods=['GET', 'POST'])
@login_required
def maketask(projectid):
    project = Project.query.get_or_404(projectid)
    if current_user != project.user:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(name=form.name.data,
                    description=form.description.data,
                    projectid=projectid)
        project.completed = 'No'
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks', projectid=projectid))
    return render_template('maketask.htm', form=form)


@app.route('/tasks/<projectid>', methods=['GET', 'POST'])
@login_required
def tasks(projectid):
    tasks = Task.query.filter_by(projectid=projectid)
    taskss = []
    for task in tasks:
        taskss.append(task)
    taskss.reverse()
    na = 'No'
    nas = 'NO'
    return render_template('tasks.htm', tasks=taskss, projectid=projectid, na=na, nas=nas)


@app.route('/task/<task_id>', methods=['GET', 'POST'])
@login_required
def task(task_id):
    task = Task.query.get(task_id)
    print(task_id)
    if task.completed == 'No':
        Status = 'Not started'
    else:
        Status = 'Completed'
    return render_template('task.htm', task=task, Status=Status)


@app.route('/change/<to>/<task_id>', methods=['GET', 'POST'])
@login_required
def change(to, task_id):
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
    return redirect(url_for('edit_task', projectid=project.id))


@app.route('/del/task/<task_id>/<projectid>', methods=['GET', 'POST'])
@login_required
def del_task(task_id, projectid):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('edit_task', projectid=projectid))


@app.route('/del/project/<projectid>', methods=['GET', 'POST'])
@login_required
def del_project(projectid):
    project = Project.query.get(projectid)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('edit_project'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/<task_id>/update', methods=['GET', 'POST'])
@login_required
def update(task_id):
    task = Task.query.get_or_404(task_id)
    form = UpdateTask()
    print('noob')
    if form.validate_on_submit():
        print('op')
        task.name = form.name.data
        task.description = form.description.data
        task.completed = form.status.data
        db.session.commit()
        return redirect(url_for('edit_task', projectid=task.project.id))
    elif request.method == 'GET':
        form.name.data = task.name
        form.description.data = task.description
        form.status.data = task.completed
    return render_template('update.htm', form=form, task_id=task_id, projectid=task.project.id)


@app.route('/queryform', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save('Tool/static/csvs/' + current_user.username + '.csv')
            return redirect(url_for('dashboard'))
    return render_template('query.htm')


@app.route('/querytableform', methods=['GET', 'POST'])
@login_required
def upload_file_create_table():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save('Tool/static/csvs/' + current_user.username +
                      'table_create' + '.csv')
            return redirect(url_for('create_table'))
    return render_template('query.htm')


@app.route('/querywhereform', methods=['GET', 'POST'])
@login_required
def upload_file_create_where():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save('Tool/static/csvs/' +
                      current_user.username + 'where' + '.csv')
            return redirect(url_for('create_where'))
    return render_template('query.htm')


if __name__ == '__main__':
    app.run(debug=True)
