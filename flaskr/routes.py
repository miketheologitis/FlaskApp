from flaskr import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from flaskr.models import Product, User, Cart, CartsProductsAssociation, Role
from flaskr.forms import RegisterForm, LoginForm, UpdateUserForm, ProductForm, SearchProductForm
from flask_login import login_user, logout_user, login_required, current_user
from random import randint


def random_unused_barcode():
    """ Returns a random unused 12 digit string barcode for products """
    barcode = str(randint(pow(10, 11), pow(10, 12)-1))
    return barcode if not Product.query.filter_by(product_code=barcode).one_or_none() else random_unused_barcode()


@app.route("/")
@app.route("/home")
@login_required
def home_page():
    """ Route that servers the home page. (home.html) """
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    """ Route that handles the login page. (login.html) """
    form = LoginForm()
    if form.validate_on_submit():  # No empty fields etc.
        user = User.query.filter_by(username=form.username.data).one_or_none()  # find user with this username
        if user and user.correct_password(form.password.data):  # If we have a tuple, Check if password hashes match
            if not user.confirmed:  # If user not authenticated by admin, deny access
                flash(f"Correct username and password but in order to login you must first be authenticated. "
                      "Contact the Admin!", category='danger')
            else:
                login_user(user)  # !!!login the user!!!
                flash(f"Success! You are logged in as {user.username}!", category='success')
                return redirect(url_for('home_page'))
        else:
            flash(f"Incorrect username or password. Please try again!", category='danger')
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for("login_page"))


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    """ Route that handles the register page. (register.html) """
    form = RegisterForm()

    if form.validate_on_submit():  # If form validated (correct email, not in database, etc.)
        # Create the new user
        new_user = User(
            name=form.name.data,
            surname=form.surname.data,
            username=form.username.data,
            passwrd=form.password1.data,  # getter/setter hashed password
            email=form.email.data,
            role=form.role.data,
            confirmed=False
        )
        db.session.add(new_user)

        if form.role.data == "USER":
            # Create the cart of the user
            new_cart = Cart(
                user_cart=new_user
            )
            db.session.add(new_cart)

        # Commit to db
        db.session.commit()

        flash(f"Success! You created an account, please wait for Admin authorization.", category='success')
        return redirect(url_for('login_page'))

    if form.errors:  # errors from the validation
        for error in form.errors.values():
            flash(f'There was an error with creating the user: {error}', category='danger')

    return render_template('register.html', form=form)


@app.route("/cart")
@login_required
def cart_page():
    """ Route that servers the cart page. (cart.html) """
    if current_user.role is not Role.USER:  # Only admin can access this
        flash(f"Unauthorized access attempt to this page. You are not a {Role.USER.value}!", category="info")
        return redirect(url_for('home_page'))
    return render_template('cart.html')


@app.route("/remove_product_from_cart", methods=['POST'])
@login_required
def remove_product_from_cart():
    """ Background ajax job to asynchronously remove a product from the cart """
    if request.method == 'POST':
        prod_id = int(request.form.get('prod_id'))
        cart_id = int(request.form.get('cart_id'))
        CartsProductsAssociation.query.filter_by(cart_id=cart_id).filter_by(product_id=prod_id).delete()
        db.session.commit()
        flash(f"Success! You successfully removed the product with ID = {prod_id} from your cart.", category='success')
        return jsonify(success=True)


@app.route("/add_product_to_cart", methods=['POST'])
@login_required
def add_product_to_cart():
    """ Background ajax job to asynchronously add a product to the cart """
    if request.method == 'POST':
        prod_id = int(request.form.get('prod_id'))
        prod = Product.query.get(prod_id)  # get the product of the form
        form_cart_id = current_user.cart.id  # current user (session) id

        query_exists = CartsProductsAssociation.query.filter_by(cart_id=form_cart_id).filter_by(product_id=prod_id)
        if query_exists.one_or_none():  # Means this product is already in our cart
            flash(f"The product {prod.name} is already in your cart. Please choose another product.", category='danger')
        else:
            new_carts_products_assoc = CartsProductsAssociation(  # the new product to insert in our cart
                cart_id=form_cart_id,
                product_id=prod_id
            )
            db.session.add(new_carts_products_assoc)
            db.session.commit()
            flash(f"Success! You have added {prod.name} in your cart.", category='success')
        return jsonify(success=True)


@app.route("/market", methods=['GET', 'POST'])
@login_required
def market_page():
    """ Route that handles the market page and the search engine. (market.html) """
    search_form = SearchProductForm()

    # https://stackoverflow.com/questions/18290142/multiple-forms-in-a-single-page-using-flask-and-wtforms
    # This is how we use two forms. See above
    if search_form.validate_on_submit():  # Means we used search engine
        products = Product.query  # build initial query
        if search_form.product_name.data:  # if there is data in product_name
            # Build query with 'Product.name LIKE %product_name%'
            products = products.filter(
                Product.name.like(
                    f"%{search_form.product_name.data}%"
                )
            )
        if search_form.category.data:  # if there is data in category
            # Build query with 'Product.category LIKE %category%'
            products = products.filter(
                Product.category.like(
                    f"%{search_form.category.data}%"
                )
            )
        if search_form.lowest_price.data:  # if there is data in lower_price
            products = products.filter(
                Product.price >= search_form.lowest_price.data
            )
        if search_form.highest_price.data:  # if there is data in highest_price
            products = products.filter(
                Product.price <= search_form.highest_price.data
            )
        # if there is data in seller_name OR seller_surname
        if search_form.seller_name.data or search_form.seller_surname.data:
            # if there is data in seller_name AND seller_surname
            if search_form.seller_name.data and search_form.seller_surname.data:
                # Join running query with Users (obviously on id), and filter resulting query with
                # 'User.name LIKE %seller_name%  AND  User.surname LIKE %seller_surname%'
                products = products.join(User).filter(
                    User.name.like(f'%{search_form.seller_name.data}%'),
                    User.surname.like(f'%{search_form.seller_surname.data}%')
                )
            # if there is data only in seller_name
            elif search_form.seller_name.data:
                # Join running query with Users (obviously on id), and filter resulting query with
                # 'User.name LIKE %seller_name%'
                products = products.join(User).filter(
                    User.name.like(f'%{search_form.seller_name.data}%')
                )
            # if there is data only in seller_surname
            else:
                # Join running query with Users (obviously on id), and filter resulting query with
                # 'User.name LIKE %seller_name%'
                products = products.join(User).filter(
                    User.surname.like(f'%{search_form.seller_surname.data}%')
                )
        if search_form.after_than_date.data:  # if there is data in after_than_date
            products = products.filter(
                Product.date_of_withdrawal >= search_form.after_than_date.data
            )
        if search_form.before_than_date.data:  # if there is data in before_than_date
            products = products.filter(
                Product.date_of_withdrawal <= search_form.before_than_date.data
            )
        products = products.all()
    else:
        products = Product.query.all()

    if search_form.errors:  # errors from the validation
        for error in search_form.errors.values():
            flash(f'There was an error with creating the product: {error}', category='danger')

    if current_user.role is Role.USER:
        #  Get all the products that are in the cart of the current user. (Will be used in html/jinja)
        current_user_cart_prods = Product.query.filter(
            Product.id.in_(
                db.session.query(CartsProductsAssociation.product_id).filter_by(
                    cart=current_user.cart
                )
            )
        )
    else:
        current_user_cart_prods = []
    return render_template('market.html', products=products,
                           search_form=search_form, current_user_cart_prods=current_user_cart_prods)


@app.route("/selling-products")
@login_required
def sell_page():
    """ Route that servers the selling-products page (for product-sellers). (selling-products.html) """
    if current_user.role is not Role.PRODUCTSELLER:  # Only admin can access this
        flash(f"Unauthorized access attempt to this page. You are not a {Role.PRODUCTSELLER.value}!", category="info")
        return redirect(url_for('home_page'))

    return render_template('selling-products.html')


@app.route('/create-product', methods=['GET', 'POST'])
@login_required
def create_product_page():
    """ Route that handles the create-product page (for product-sellers). (create-product.html) """
    if current_user.role is not Role.PRODUCTSELLER:  # Only admin can access this
        flash(f"Unauthorized access attempt to this page. You are not a {Role.PRODUCTSELLER.value}!", category="info")
        return redirect(url_for('home_page'))

    form = ProductForm()

    # https://stackoverflow.com/questions/63434291/add-a-cancel-button-in-flask-with-flask-wtf-wtforms
    # Cancel button implementation. Dodge the validators and redirect.
    if request.method == 'POST':
        if form.cancel.data:
            flash("Product listing was cancelled.", category="info")
            return redirect(url_for('sell_page'))

    if form.validate_on_submit():
        if form.submit.data:
            new_product = Product(
                name=form.name.data,
                product_code=random_unused_barcode(),
                price=form.price.data,
                date_of_withdrawal=form.date_of_withdrawal.data,
                seller_id=current_user.id,
                category=form.category.data
            )
            db.session.add(new_product)
            db.session.commit()

            flash("Successfully added your product in the marketplace.", "success")
            return redirect(url_for('market_page'))

    if form.errors:  # errors from the validation
        for error in form.errors.values():
            flash(f'There was an error with creating the product: {error}', category='danger')

    return render_template('create-product.html', form=form)


@app.route('/delete_product', methods=['POST'])
@login_required
def delete_product():
    """ Background ajax job to asynchronously delete a product (as a product-seller)"""
    if request.method == 'POST':
        prod_id = int(request.form.get('prod_id'))
        Product.query.filter_by(id=prod_id).delete()
        db.session.commit()
        flash(f"Success! Deleted product with ID = {prod_id}.", category='success')
        return jsonify(success=True)


@app.route('/update-product/<prod_id>', methods=['GET', 'POST'])
@login_required
def update_product_page(prod_id):
    """ Route that handles the update-product page (for product-sellers). (update-product .html) """
    if current_user.role is not Role.PRODUCTSELLER:  # Only admin can access this
        flash(f"Unauthorized access attempt to this page. You are not a {Role.PRODUCTSELLER.value}!", category="info")
        return redirect(url_for('home_page'))

    form = ProductForm()

    product = Product.query.get(prod_id)

    # https://stackoverflow.com/questions/63434291/add-a-cancel-button-in-flask-with-flask-wtf-wtforms
    # Cancel button implementation. Dodge the validators and redirect.
    if request.method == 'POST':
        if form.cancel.data:
            flash("Product update was cancelled.", category="info")
            return redirect(url_for('sell_page'))

    if form.validate_on_submit():
        if form.submit.data:
            # Update product in db
            product.name = form.name.data
            product.price = form.price.data
            product.category = form.category.data
            db.session.commit()

            flash("Successfully updated your product.", "success")
            return redirect(url_for('sell_page'))

    return render_template('update-product.html', form=form, product=product)


@app.route("/manage-users")
@login_required
def manage_users_page():
    """ Route that servers the manage-users page (for admin). (manage-users.html) """
    if current_user.role is not Role.ADMIN:  # Only admin can access this
        flash(f"Unauthorized access attempt to this page. You are not a {Role.ADMIN.value}!", category="info")
        return redirect(url_for('home_page'))
    return render_template('manage-users.html', users=User.query.all())


@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    """ Background ajax job to asynchronously delete a user (as admin) """
    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        User.query.filter_by(id=user_id).delete()
        db.session.commit()
        flash(f"Success! Deleted user with ID = {user_id}.", category='success')
        return jsonify(success=True)


@app.route('/confirm_user', methods=['POST'])
@login_required
def confirm_user():
    """ Background ajax job to asynchronously confirm a user (as admin) """
    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        user = User.query.get(user_id)
        user.confirmed = True  # Update
        db.session.commit()
        flash(f"Success! Confirmed user with ID = {user_id}.", category='success')
        return jsonify(success=True)


@app.route("/update-user/<user_id>", methods=['GET', 'POST'])
@login_required
def update_user_page(user_id):
    """ Route that handles the update-user page (for admin). (update-user.html) """
    if current_user.role is not Role.ADMIN:  # Only admin can access this
        flash(f"Unauthorized access attempt to this page. You are not a {Role.ADMIN.value}!", category="info")
        return redirect(url_for('home_page'))

    user = User.query.get(user_id)
    if not user:  # Check if user id exists. Defend against custom URLs.
        flash("The User ID you are trying to update does not exist. "
              "Please follow the website's links. Do not type custom URLs.!", category="danger")
        return redirect(url_for('manage_users_page'))

    form = UpdateUserForm(role=user.role.value)

    # https://stackoverflow.com/questions/63434291/add-a-cancel-button-in-flask-with-flask-wtf-wtforms
    # Cancel button implementation. Dodge the validators and redirect.
    if request.method == 'POST':
        if form.cancel.data:
            flash("No updates have been implemented.", category="info")
            return redirect(url_for('manage_users_page'))

    if form.validate_on_submit():
        if form.submit.data:
            form_name = form.name.data
            form_surname = form.surname.data
            form_email = form.email.data
            form_username = form.username.data
            form_role = form.role.data

            # Check e-mail uniqueness
            if User.query.filter_by(email=form_email).filter(User.id != user.id).one_or_none():
                flash("E-mail already exists! Please try a different e-mail address!", category="danger")
                return redirect(url_for('update_user', user_id=user_id))

            # Check username uniqueness
            if User.query.filter_by(username=form_username).filter(User.id != user.id).one_or_none():
                flash("Username already exists! Please try a different username!", category="danger")
                return redirect(url_for('update_user', user_id=user_id))

            # If we change the role of the User then we need to delete/update carts/products
            # accordingly.
            if user.role.value != form_role:  # Different role
                if form_role == "ADMIN":  # Delete products/carts
                    Product.query.filter_by(seller_id=user.id).delete()  # in case user was a PRODUCTSELLER
                    Cart.query.filter_by(user_id=user.id).delete()  # in case user was a USER
                    user.confirmed = True  # admin always confirmed
                if form_role == "USER":
                    Product.query.filter_by(seller_id=user.id).delete()  # in case user was a PRODUCTSELLER
                    new_cart = Cart(  # the cart of our USER
                        user_cart=user
                    )
                    db.session.add(new_cart)
                if form_role == "PRODUCTSELLER":
                    Cart.query.filter_by(user_id=user.id).delete()  # in case user was a USER
                flash("You chose to change the role of the user. Associated instances (if any) with the "
                      "previous role were deleted.", category="info")

            # Update user
            user.name = form_name
            user.surname = form_surname
            user.email = form_email
            user.username = form_username
            user.role = form_role
            db.session.commit()  # commit all changes

            flash("User was updated successfully!", category="success")
            return redirect(url_for('manage_users_page'))

    return render_template('update-user.html', form=form, user=user)
