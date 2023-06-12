from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, PasswordField,validators,DateField
from wtforms.validators import DataRequired, Email, NumberRange


class LoginForm(FlaskForm):
    username = StringField(label = "Username", validators = [DataRequired(message = "Username is a required field.")])

    password = PasswordField(label = "Password", validators = [DataRequired(message = "Password is a required field.")])

    submit = SubmitField("Log In")
    
class ChangepasswordForm(FlaskForm):
    old_password = PasswordField(label = "Old password", validators = [DataRequired(message = "Old password is a required field.")])

    new_password = PasswordField(label = "New password", validators = [DataRequired(message = "New Password is a required field.")])

    submit = SubmitField("Change")
    
class ChangemailForm(FlaskForm):
    old_mail = StringField(label = "Old email", validators = [DataRequired(message = "Old email is a required field."), Email(message = "Invalid email format.")])
    
    new_mail = StringField(label = "New email", validators = [DataRequired(message = "New email is a required field."), Email(message = "Invalid email format.")])

    submit = SubmitField("Change")
    
    
class SearchForm(FlaskForm):
    title = StringField(label = "Book title")
    
    category = StringField(label = "Book category")
    
    author = StringField(label = "Book author")

    submit = SubmitField("Search")
    
class ReviewForm(FlaskForm):
    
    grade=IntegerField(label="Your grade",validators = [DataRequired(message = "Grade is a required field."),NumberRange(0,10,message="Grade must be between 0 and 10")])
    
    review=StringField(label="Your review")
    
    submit = SubmitField("Post")
    

class Search_op_Form(FlaskForm):
    title = StringField(label = "Book title")
    
    category = StringField(label = "Book category")
    
    author = StringField(label = "Book author")
    
    copies= IntegerField(label= "Available Copies",validators=[validators.optional()])

    submit = SubmitField("Search")
    
    
class add_book_Form(FlaskForm):
    
    ISBN = StringField(label = "Book ISBN", validators = [DataRequired(message = "ISBN is a required field.")])

    title = StringField(label = "Book title", validators = [DataRequired(message = "Title is a required field.")])
    
    publication_date = DateField(label = "Book date", validators = [DataRequired(message = "Publication date is a required field.")])
    
    publisher = StringField(label = "Book publisher", validators = [DataRequired(message = "Publisher is a required field.")])
    
    number_of_pages = IntegerField(label = "Number of pages", validators = [DataRequired(message = "Number of pages is a required field.")])
    
    summary = StringField(label = "Summary", validators = [DataRequired(message = "Summary is a required field.")])
    
    available_copies = IntegerField(label = "Available copies", validators = [DataRequired(message = "Available copies is a required field.")])
    
    language = StringField(label = "Language", validators = [DataRequired(message = "Language is a required field.")])
    
    keywords = StringField(label = "Keyword", validators = [DataRequired(message = "Keywords is a required field.")])
    
    first_name = StringField(label = "Author first name", validators = [DataRequired(message = "First name is a required field.")])

    last_name = StringField(label = "Author last name", validators = [DataRequired(message = "Last name is a required field.")])

    category = StringField(label = "Category", validators = [DataRequired(message = "Category is a required field.")])

    submit = SubmitField("Add")

class return_book_Form(FlaskForm):
    
    id_user= IntegerField(label = "User ID", validators = [DataRequired(message = "User ID is a required field.")])

    ISBN = StringField(label = "Category", validators = [DataRequired(message = "ISBN is a required field.")])

    submit = SubmitField("Return")
    
class check_user_Form(FlaskForm):
    
    first_name = StringField(label = "First name")
    
    last_name = StringField(label = "Last name")
    
    submit=SubmitField("search")
    
    
class rating_book_Form(FlaskForm):
    
    id_user= IntegerField(label= "User ID",validators=[validators.optional()])
    
    category = StringField(label = "Category")
    
    submit=SubmitField("search")
    
    
class school_loans_Form(FlaskForm):
    
    year= IntegerField(label= "Year",validators=[validators.optional()])
    
    month= IntegerField(label= "Month",validators=[validators.optional(),NumberRange(1,12,message="Month must be between 1 and 12")])
    
    submit=SubmitField("search")    

class operator_loans_Form(FlaskForm):
    
    year= IntegerField(label= "Year",validators=[validators.optional()])
        
    submit=SubmitField("search")    
    
class affiliation_category_Form(FlaskForm):
    
    category= StringField(label= "Category")
        
    submit=SubmitField("search")    
    

class add_school_Form(FlaskForm):
    
    name = StringField(label = "School name", validators = [DataRequired(message = "School name is a required field.")])
    
    address = StringField(label = "Address", validators = [DataRequired(message = "Adress is a required field.")])
    
    city =StringField(label = "School city", validators = [DataRequired(message = "City is a required field")])
    
    email = StringField(label = "Email", validators = [DataRequired(message = "Email is a required field."), Email(message = "Invalid email format.")])
    
    director_name = StringField(label = "Director name", validators = [DataRequired(message = "Director name is a required field.")])

    phone_number = IntegerField(label = "Phone number", validators = [DataRequired(message = "Phone number is a required field.")])
    
    id_admin=IntegerField(label = "Admin ID", validators = [DataRequired(message = "Admin ID is a required field.")])
    
    id_operator=IntegerField(label = "Operator ID", validators = [DataRequired(message = "Operator ID is a required field.")])
        
    submit = SubmitField("Add") 
    
    
class add_operator_Form(FlaskForm):
    
    first_name = StringField(label = "First name", validators = [DataRequired(message = "First name is a required field.")])
    
    last_name = StringField(label = "Last name", validators = [DataRequired(message = "Last name is a required field.")])
    
    birth_date=DateField(label = "Birth date", validators = [DataRequired(message = "Birth date is a required field")])
    
    email = StringField(label = "Email", validators = [DataRequired(message = "Email is a required field."), Email(message = "Invalid email format.")])
    
    username = StringField(label = "Username", validators = [DataRequired(message = "Username is a required field.")])

    password = PasswordField(label = "Password", validators = [DataRequired(message = "Password is a required field.")])
    
    submit = SubmitField("Add")
    
    

    