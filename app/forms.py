from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class UserRegistration(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=5, max=10)] )
    first_name = StringField('Firstname', 
                           validators=[DataRequired(), Length(min=5, max=50)] )
    last_name = StringField('Lastname', 
                           validators=[DataRequired(), Length(min=5, max=50)] )
    email = StringField('Email', validators=[DataRequired(), Email()] )
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('ConfirmPassword', validators=[DataRequired(), EqualTo('Password')])
    phone = IntegerField('Phone', validators=[DataRequired(), Length(min=11, max=11)])
    submit = SubmitField('Sign Up')
    
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken!")
    
    
class UserLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()] )
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    
# class AdminRegistration(FlaskForm):
#     username = StringField('Username', 
#                            validators=[DataRequired(), Length(min=5, max=10)] )
#     # first_name = StringField('Firstname', 
#     #                        validators=[DataRequired(), Length(min=5, max=50)] )
#     # last_name = StringField('Lastname', 
#     #                        validators=[DataRequired(), Length(min=5, max=50)] )
#     email = StringField('Email', validators=[DataRequired(), Email()] )
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('ConfirmPassword', validators=[DataRequired(), EqualTo('Password')])
#     submit = SubmitField('Sign Up')
    
#     def validate_email(self, email):
#         if User.query.filter_by(email=email.data).first():
#             raise ValidationError("Email already registered!")

#     def validate_uname(self, username):
#         if User.query.filter_by(username=username.data).first():
#             raise ValidationError("Username already taken!")
    
    
# class AdminLogin(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()] )
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Login')