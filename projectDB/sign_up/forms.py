from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, PasswordField, DateField
from wtforms.validators import DataRequired, Email


class SignUpForm(FlaskForm):
    first_name = StringField(label = "First name", validators = [DataRequired(message = "First name is a required field.")])
    
    last_name = StringField(label = "Last name", validators = [DataRequired(message = "Last name is a required field.")])
    
    birth_date=DateField(label = "Birth date", validators = [DataRequired(message = "Birth date is a required field")])
    
    email = StringField(label = "Email", validators = [DataRequired(message = "Email is a required field."), Email(message = "Invalid email format.")])
    
    username = StringField(label = "Username", validators = [DataRequired(message = "Username is a required field.")])

    password = PasswordField(label = "Password", validators = [DataRequired(message = "Password is a required field.")])
    
    role = SelectField(label="Role",validators = [DataRequired(message = "Role is a required field.")],choices=["student","teacher"])
    
    schools = SelectField(label="School",coerce=str,validators = [DataRequired(message = "School is a required field.")])
    
    submit = SubmitField("Sign Up")