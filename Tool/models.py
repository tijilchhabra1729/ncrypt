from Tool import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64))
    username = db.Column(db.String , unique = True)
    profile_image = db.Column(db.String(64), nullable = False , default = 'developer.png')
    email = db.Column(db.String(64),unique = True,index = True)
    password_hash = db.Column(db.String(128))

    project = db.relationship('Project' , backref = 'user' , lazy = 'dynamic')


    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __init__(self, name,username, email, password ):
        self.email = email
        self.name =name
        self.username = username
        self.password_hash = generate_password_hash(password)

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    completed = db.Column(db.String , default = 'No')

    userid = db.Column(db.Integer , db.ForeignKey('users.id'))
    tasks = db.relationship('Task' , backref = 'project' , lazy = 'dynamic')

    def __init__(self , name , description , userid):
        self.name = name
        self.description = description
        self.userid = userid

class Task(db.Model):
    __tablename__= 'tasks'
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    completed = db.Column(db.String , default = 'No')

    projectid = db.Column(db.Integer , db.ForeignKey('project.id'))

    def __init__(self, name, description , projectid):
        self.name = name
        self.description = description
        self.projectid = projectid
