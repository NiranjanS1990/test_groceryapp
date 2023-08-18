from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField,DateField,SearchField
from wtforms.validators import Length, EqualTo, Email, DataRequired,ValidationError
from flask_wtf.file import FileAllowed,FileRequired, FileField
from wtforms_sqlalchemy.fields import QuerySelectField
from grocery import photos
from grocery.models import User,Item,Category

class RegisterForm(FlaskForm):
  def validate_username(self, username_to_check):
    user = User.query.filter_by(username=username_to_check.data).first()
    if user:
        raise ValidationError('Username already exists! Please try a different username')

  def validate_email_address(self, email_address_to_check):
    email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
    if email_address:
        raise ValidationError('Email Address already exists! Please try a different email address')
  username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
  email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
  password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
  password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
  submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class CategoryForm(FlaskForm):
  def validate_name(self, category_to_check):
    name = Category.query.filter_by(name=category_to_check.data).first()
    if name:
      raise ValidationError('CategoryName already exists! Please try a different Name')
  name = StringField(label='Category:', validators=[Length(max=30), DataRequired()])
  description = StringField(label='Description:', validators=[Length(max=1024)])
  submit = SubmitField(label='Add Data')


def Category_query():
    return Category.query
  
class ItemForm(FlaskForm):
  def validate_product(self, product_to_check):
    product = Item.query.filter_by(product=product_to_check.data).first()
    if product:
        raise ValidationError('ProductName already exists! Please try a different Name')

  product = StringField(label='Product:', validators=[Length(max=30), DataRequired()])
  price = IntegerField(label='Amount:', validators=[DataRequired()])
  category = QuerySelectField(label='Category:',query_factory=Category_query,allow_blank=False, get_label='name', validators=[DataRequired()])
  quantity_stored = IntegerField(label="Quantity added",validators=[DataRequired()])
  unit = StringField(label="Unit",validators=[DataRequired()])
  manufacture_date = DateField(label="Mfd",validators=[DataRequired()])
  expiry_date = DateField(label="Exd",validators=[DataRequired()])
  description = StringField(label='Description:', validators=[Length(max=1024)])
  photo=FileField(label="Upload Photo",validators=[FileAllowed(photos),FileRequired("FileField should not be empty")])
  submit = SubmitField(label='Add Data')



class ItemForm_update(FlaskForm):
  product = StringField(label='Product:', validators=[Length(max=30), DataRequired()])
  price = IntegerField(label='Amount:', validators=[DataRequired()])
  category = QuerySelectField(label='Category:',query_factory=Category_query,allow_blank=False, get_label='name', validators=[DataRequired()])
  quantity_stored = IntegerField(label="Quantity added",validators=[DataRequired()])
  unit = StringField(label="Unit",validators=[DataRequired()])
  manufacture_date = DateField(label="Mfd",validators=[DataRequired()])
  expiry_date = DateField(label="Exd",validators=[DataRequired()])
  description = StringField(label='Description:', validators=[Length(max=1024)])
  submit = SubmitField(label='Add Data')



#Search form
class SearchForm(FlaskForm):
  search_object= SearchField(label="Search for Products...", validators=[ DataRequired()])
  submit = SubmitField(label='Search')

class Cat_SearchForm(FlaskForm):
  category_search =  QuerySelectField(label='Category:',query_factory=Category_query,allow_blank=False, get_label='name')
  submit = SubmitField(label='Search')
  
    
class CartForm(FlaskForm):
  user_id = IntegerField(label="user_id",validators=[DataRequired()])
  product_id=IntegerField(Label="product_id",validators=[DataRequired()])
  submit = SubmitField(label='Submit')
  
  




