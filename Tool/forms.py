from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,SubmitField , TextAreaField , FileField , IntegerField , RadioField , DateField
from wtforms.validators import DataRequired, Email , EqualTo, Length
from flask_wtf.file import FileField,FileAllowed
from wtforms import ValidationError

from flask_login import current_user
from Tool.models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    name = StringField('First Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('pass_confirm', message='Passwords must match'), Length(min = 8, max=16)])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    picture = FileField(' Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email you chose has already been registered')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The username you chose has already been registered')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class ProjectForm(FlaskForm):
    name = StringField('Project Name' , validators=[DataRequired()])
    description = TextAreaField('Project Description' , validators=[DataRequired()])
    submit = SubmitField('Make Project')

class TaskForm(FlaskForm):
    name = StringField('Task Name' , validators=[DataRequired()])
    description = TextAreaField('Task Description' , validators=[DataRequired()])
    submit = SubmitField('Add task')
class QueryForm(FlaskForm):
    data_input = FileField('Data', validators=[
                           FileAllowed(['csv']), DataRequired()])
    submit = SubmitField('Upload Data')
class QueryReq(FlaskForm):
    table_name = StringField('Table Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class QueryReqWhere(FlaskForm):
    table_name = StringField('Table Name', validators=[DataRequired()])
    value = StringField('Value', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UpdateQuery(FlaskForm):
    table_name = StringField('Table Name', validators=[DataRequired()])
    column_name = StringField('Column Name' , validators=[DataRequired()])
    changed_val = StringField('Changed Value' , validators=[DataRequired()])
    submit = SubmitField('Submit')

class UpdateTask(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = RadioField('Status', choices=[('Yes','completed'),('No','not completed') , ('Maybe' , 'In progress')])
    submit = SubmitField('Update')
