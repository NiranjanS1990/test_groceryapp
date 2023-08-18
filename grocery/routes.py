from grocery import app, db, photos
from flask import render_template, redirect, url_for, flash, request,make_response
from grocery.models import User, Item, Category, Cart,cart_product,Order,order_product,login_count
from grocery.forms import RegisterForm, LoginForm, ItemForm, CategoryForm, SearchForm,Cat_SearchForm,ItemForm_update
from flask_login import login_user, login_required, logout_user, current_user
#from grocery.api_routes import api
#api.init_app(app)
#from weasyprint import HTML



@app.route('/home')
def home_page():
  return render_template('home.html')


@app.route("/dashboard")
@login_required
def dashboard():
  form3 = SearchForm()
  form4=Cat_SearchForm()
  cart = Cart.query.filter_by(user_id=current_user.id).first()
  item_count = len(cart.products)
  products = Item.query.all()
  Categories = Category.query.all()
  return render_template("dashboard.html",
                         products=products,
                         Categories=Categories,
                         form3=form3,
                         form4=form4,
                         cart=cart,
                         item_count=item_count)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
  form = RegisterForm()
  if form.validate_on_submit():
    user_to_create = User(username=form.username.data,
                          email_address=form.email_address.data,
                          password=form.password1.data)
    db.session.add(user_to_create)
    db.session.commit()
    return redirect(url_for('home_page'))
  if form.errors != {}:  #If there are not errors from the validations
    for err_msg in form.errors.values():
      flash(f'There was an error with creating a user: {err_msg}')

  return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
  form = LoginForm()
  if form.validate_on_submit():
    attempted_user = User.query.filter_by(username=form.username.data).first()
    if attempted_user and attempted_user.check_password_correction(
        attempted_password=form.password.data):
      login_user(attempted_user)
      #flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
      cart = Cart(user_id=current_user.id)
      db.session.add(cart)
      db.session.commit()
      obj = login_count.query.filter_by(user_id=current_user.id).first()
      if obj:
        obj.count = obj.count + 1
        db.session.commit()
      else:
        obj = login_count(user_id=current_user.id, count=1)
        db.session.add(obj) 
        db.session.commit()
      if current_user.id == 1:
        return redirect(url_for('admin_dashboard'))
      return redirect(url_for('dashboard'))
    else:
      flash('Username and password are not match! Please try again',
            category='danger')
  return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
  logout_user()
  flash("You have been logged out!", category='info')
  return redirect(url_for("home_page"))


@app.route('/admin-dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
  if current_user.id == 1:
    products = Item.query.all()
    form = ItemForm()
    Categories = Category.query.all()
    form.category.query = Categories
    form1 = ItemForm_update()
    form2 = CategoryForm()
    form3 = SearchForm()
    form5 = CategoryForm()
    form4=Cat_SearchForm()
    if form.validate_on_submit():
      file_name = photos.save(form.photo.data)
      product_to_create = Item(product=form.product.data,
                               price=form.price.data,
                               category=form.category.data,
                               manufacture_date=form.manufacture_date.data,
                               expiry_date=form.expiry_date.data,
                               photo_dest_path=f"upload/{file_name}",
                               quantity_stored=form.quantity_stored.data,
                               unit=form.unit.data,
                               description=form.description.data)
  
      db.session.add(product_to_create)
      db.session.commit()
      flash("Item added successfully")
      return redirect(url_for('admin_dashboard'))
    if form.errors != {}:  #If there are not errors from the validations
      for err_msg in form.errors.values():
        flash(f'There was an error with creating a item: {err_msg}')
    return render_template("admin_dashboard.html",
                           form=form,
                           products=products,
                           form1=form1,
                           form2=form2,
                           form3=form3,
                           form4=form4,form5=form5,
                           Categories=Categories)
  else:
    flash('Only Admin can acess the page')
    return redirect(url_for('login_page'))


@app.route('/admin-dashboard/category', methods=["Get", "Post"])
def categories():
  form2 = CategoryForm()
  if form2.validate_on_submit():
    category_to_create = Category(name=form2.name.data,
                                  description=form2.description.data)
    db.session.add(category_to_create)
    db.session.commit()
    flash("Item added successfully")
    return redirect(url_for('admin_dashboard'))
  if form2.errors != {}:  #If there are not errors from the validations
    for err_msg in form2.errors.values():
      flash(f'There was an error with creating a item: {err_msg}')
  return redirect(url_for('admin_dashboard'))


@app.route('/admin-dashboard/category/<id>', methods=["Post"])
def update_categories(id):
  form4 = CategoryForm()
  Category_to_update = Category.query.get(id)
  if form4.validate_on_submit():
    Category_to_update.name = form4.name.data
    Category_to_update.description = form4.description.data
    db.session.commit()
    return redirect(url_for('admin_dashboard'))
  return redirect(url_for('admin_dashboard'))


@app.route("/admin-dashboard/Cat_delete/<id>", methods=["Get", "POST"])
def delete_categories(id):
  Category_to_delete = Category.query.get(id)
  db.session.delete(Category_to_delete)
  db.session.commit()
  return redirect(url_for('admin_dashboard'))


@app.route('/admin-dashboard/update/<id>', methods=['GET', 'POST'])
def update(id):
  form1 = ItemForm_update()
  product_to_update = Item.query.get(id)
  if form1.validate_on_submit():
    #file_name = photos.save(form1.photo.data)
    product_to_update.product = form1.product.data
    product_to_update.category = form1.category.data
    product_to_update.manufacture_date = form1.manufacture_date.data
    product_to_update.expiry_date = form1.expiry_date.data
    product_to_update.description = form1.description.data
    #product_to_update.photo_dest_path = f"upload/{file_name}"
    #db.session.update(product_to_update)
    product_to_update.quantity_stored = form1.quantity_stored.data
    product_to_update.unit = form1.unit.data
    product_to_update.price = form1.price.data
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

  return redirect(url_for('admin_dashboard'))


@app.route("/admin-dashboard/delete/<id>", methods=["Get", "POST"])
def delete(id):
  product_to_delete = Item.query.get(id)
  db.session.delete(product_to_delete)
  db.session.commit()
  return redirect(url_for('admin_dashboard'))


@app.route("/admin-search", methods=["Post"])
def search():
  form = ItemForm()
  form1 = ItemForm_update()
  form2 = CategoryForm()
  form3 = SearchForm()
  form4=Cat_SearchForm()
  #products = Item.query
  if form3.validate_on_submit():
    searched = form3.search_object.data
    products = Item.query.filter(Item.product.like(f"%{searched}%")).all()
    return render_template("search_admin.html",
                           form3=form3,
                           searched=searched,
                           products=products,
                           form=form,
                           form1=form1,
                           form2=form2,form4=form4)


@app.route("/admin-dashboard/category-search",methods=["Get", "POST"])
def cat_search():
  form = ItemForm()
  form1 = ItemForm_update()
  form2 = CategoryForm()
  form3 = SearchForm()
  form4=Cat_SearchForm()
  if form4.validate_on_submit():
    category=form4.category_search.data
    #category = Category.query.filter_by(name=category).first()
    products = category.items
    return render_template("search_admin.html",
                           products=products,
                           searched=category,
                           form4=form4,
                           form=form,
                           form1=form1,
                           form2=form2,form3=form3)
  




@app.route("/user-search", methods=["Post"])
def user_search():
  form3 = SearchForm()
  form4=Cat_SearchForm()
  #Categories=Category.query.all()
  if form3.validate_on_submit():
    searched = form3.search_object.data
    products = Item.query.filter(Item.product.like(f"%{searched}%")).all()
    return render_template("search_user.html",
                           form3=form3,
                           form4=form4,
                           searched=searched,
                           products=products)

@app.route("/dashboard/category-search",methods=["Get", "POST"])
def user_cat_search():
  form3 = SearchForm()
  form4=Cat_SearchForm()
  if form4.validate_on_submit():
    category=form4.category_search.data
    #category = Category.query.filter_by(name=category).first()
    products = category.items
    return render_template("search_user.html",
                           products=products,
                           searched=category,
                           form4=form4,
                           form3=form3)
  





@app.route("/dashboard/<id>", methods=["POST"])
def add_to_cart(id):
  try:
      if request.method == 'POST':
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        Product = Item.query.get(id)
        quantity = int(request.form.get('quantity'))
        # Checking if quantity does not exceed stock
        if Product.quantity_stored >= quantity:
          cart_product_ = cart_product.insert().values(cart_id=cart.id, product_id=Product.id, quantity=quantity)
          db.session.execute(cart_product_)
          db.session.commit()
          flash(f"Success! You have added {Product.product} to cart")
          return redirect(url_for('dashboard'))
        else:
          flash(f'Only {Product.quantity_stored} quantity of {Product.product} is available in stock')
          return redirect(url_for('dashboard'))
  except Exception as e:
      flash("An error occurred while adding the product to the cart.")
      # You may want to log the error or handle it differently
  return redirect(url_for('dashboard'))



@app.route("/dashboard/cart")
def cart():
  form3 = SearchForm()
  form4=Cat_SearchForm()
  Products_purchased={'product':[],'quantity':[]}
  cart = Cart.query.filter_by(user_id=current_user.id).first()
  products=cart.products
  items_in_cart=len(products)
  Total_cost=0
  user=login_count.query.filter_by(user_id=current_user.id).first()
  count=user.count
  if count ==1:
    discount = 0.20
  else:
    discount = 0
  for Product in products:
    Products_purchased['product'].append(Product)
    #last_entry = db.session.query(cart_product).order_by(cart_product.id.desc()).first()
    #quantity = last_entry.quantity
    last_entry = db.session.query(cart_product).filter_by(product_id=Product.id).order_by(cart_product.c.id.desc()).first()
    quantity = last_entry.quantity
    Products_purchased['quantity'].append(quantity)
    Total_cost+=Product.price*quantity*(1-discount)
  return render_template('cart.html',
                         Products_purchased=Products_purchased,
                         Total_cost=Total_cost,
                         form3=form3,
                         form4=form4,
                         items_in_cart=items_in_cart,
                        discount=discount)


@app.route('/cart/<int:product_id>/remove', methods=["POST", "GET"])
def remove_from_cart(product_id):
  db.session.query(cart_product).filter_by(product_id=product_id).delete()
  db.session.commit()
  return redirect(url_for('cart'))


@app.route('/cart/clear', methods=["POST", "GET"])
def clear_cart():
  user_id = current_user.id
  cart = Cart.query.filter_by(user_id=user_id).first()
  db.session.query(cart_product).filter_by(cart_id=cart.id).delete()
  db.session.commit()
  return redirect(url_for('cart'))


@app.route('/cart/order/<amount>',methods=["POST","GET"])
def order_cart(amount):
  form3 = SearchForm()
  form4=Cat_SearchForm()
  user_id = current_user.id
  order=Order(user_id=user_id,amount=amount)
  db.session.add(order)
  db.session.commit()
  cart = Cart.query.filter_by(user_id=user_id).first()
  products=cart.products
  product_purchased={'Product':[],'quantity':[]}
  item_list=len(products)
  user=login_count.query.filter_by(user_id=current_user.id).first()
  count=user.count
  if count ==1:
    discount = 0.20
  else:
    discount = 0
  for Product in products:
    last_entry = db.session.query(cart_product).filter_by(product_id=Product.id).order_by(cart_product.c.id.desc()).first()
    quantity = last_entry.quantity
    order_product_=order_product.insert().values(order_id=order.id,     product_id=Product.id, quantity=quantity)
    product_purchased['Product'].append(Product)
    product_purchased['quantity'].append(quantity)
    Product.quantity_stored = Product.quantity_stored - quantity
    db.session.execute(order_product_)
    db.session.commit()
  db.session.query(cart_product).filter_by(cart_id=cart.id).delete()
  db.session.commit()
  return render_template('generate_pdf.html',item_list=item_list,product_purchased=product_purchased,amount=amount,order=order,form3=form3,form4=form4,discount=discount)


@app.route('/admin-dashboard/order', methods=["POST","GET"])
def orderlist():
  form = ItemForm()
  form2 = CategoryForm()
  form3 = SearchForm()
  form4=Cat_SearchForm()
  orderlist=[]
  if request.method == 'POST':
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    orderlist=Order.query.filter(Order.timestamp >= from_date,   Order.timestamp <= to_date).all()
    return render_template('orderlist.html',orderlist=orderlist,form=form,form2=form2,form3=form3,form4=form4)
  return render_template('orderlist.html',form=form,form2=form2,form3=form3,form4=form4,orderlist=orderlist)
  

'''@app.route('/admin-dashboard/order/<id>',methods=["POST","GET"])
def orderdetail(id):
  form = ItemForm()
  form2 = CategoryForm()
  form3 = SearchForm()
  form4=Cat_SearchForm()
  order=Order.query.get(id)
  products=order.products
  order_details={'product':[],'quantity':[]}
  items=len(products)
  for product in products:
    quantity_ = db.session.query(order_product).filter(order_product.order_id == id, order_product.product_id == product.id).first()
    quantity=quantity_.quantity
    order_details['product'].append(product)
    order_details['quantity'].append(quantity)
  return render_template('productlist.html',form=form,form2=form2,form3=form3,form4=form4,order_details=order_details,items=items,id=id)'''
  
  
  
