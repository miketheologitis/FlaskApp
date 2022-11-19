from flaskr import db, login_manager  # , bcrypt
import enum
from hashlib import sha256
# Ignore this comment (db. -> sqlalchemy.)


class Role(enum.Enum):
    ADMIN = "ADMIN"
    PRODUCTSELLER = "PRODUCTSELLER"
    USER = "USER"


# This callback is used to reload the user object from the user ID stored in the session.
# See https://flask-login.readthedocs.io/en/latest/#how-it-works
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # primary key query


# Association table many-to-many
# See https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
class CartsProductsAssociation(db.Model):
    __tablename__ = "carts_products"

    # The cart that this product is inside to
    # The default value of relationship.cascade is save-update, merge.
    # The typical alternative setting for this parameter is either all or more commonly all, delete-orphan.
    # The all symbol is a synonym for save-update, merge, refresh-expire, expunge, delete,
    # and using it in conjunction with delete-orphan indicates that the child object should follow along with
    # its parent in all cases, and be deleted once it is no longer associated with that parent.
    cart_id = db.Column(
        db.Integer(),
        db.ForeignKey('carts.id', ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )

    # The product that is inside this cart
    # The default value of relationship.cascade is save-update, merge.
    # The typical alternative setting for this parameter is either all or more commonly all, delete-orphan.
    # The all symbol is a synonym for save-update, merge, refresh-expire, expunge, delete,
    # and using it in conjunction with delete-orphan indicates that the child object should follow along with
    # its parent in all cases, and be deleted once it is no longer associated with that parent.
    product_id = db.Column(
        db.Integer(),
        db.ForeignKey('products.id', ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )

    # Date of insertion should be here..!
    date_of_insertion = db.Column(
        db.DateTime(timezone=False),
        server_default=db.func.current_timestamp()
    )

    cart = db.relationship(
        'Cart',
        back_populates='carts_prods',
        uselist=False
    )

    product = db.relationship(
        'Product',
        back_populates='carts_prods',
        uselist=False
    )


class User(db.Model):
    __tablename__ = "users"

    # autoincrement is True
    id = db.Column(
        db.Integer(),
        primary_key=True
    )

    name = db.Column(
        db.String(length=30),
        nullable=False
    )

    surname = db.Column(
        db.String(length=30),
        nullable=False
    )

    username = db.Column(
        db.String(length=30),
        unique=True,
        nullable=False
    )

    # password will be hashed using flask crypto
    password = db.Column(
        db.String(length=64),
        nullable=False
    )

    email = db.Column(
        db.String(length=60),
        unique=True,
        nullable=False
    )

    role = db.Column(
        db.Enum(Role),
        nullable=False
    )

    confirmed = db.Column(
        db.Boolean(),
        server_default=db.true(),  # TODO: change to false()
        nullable=False
    )

    # Relational pattern for the products of this user. One user can sell many products (many-to-one)
    # Also, for each product we have a back-reference to its owner through Product.user_seller
    products = db.relationship(
        'Product',
        back_populates='user_seller',
        cascade="all, delete"
    )

    # Relational pattern for the cart of this user. One user can have only one cart. (one-to-one)
    # Also, for each product we have a back-reference to its owner through Product.user_seller
    cart = db.relationship(
        'Cart',
        uselist=False,  # explicitly one-to-one
        back_populates='user_cart',
        cascade="all, delete"
    )

    # Getter/Setters for hashing passwords
    @property
    def passwrd(self):
        return self.password

    # Getter/Setters for hashing passwords
    @passwrd.setter
    def passwrd(self, plain_text_password):
        #self.password = bcrypt.generate_password_hash(plain_text_password)
        self.password = sha256(plain_text_password.encode('utf-8')).hexdigest()

    # This property should return True if the user is authenticated, i.e. they have provided valid credentials.
    # (Only authenticated users will fulfill the criteria of login_required.)
    # See https://flask-login.readthedocs.io/en/latest/#how-it-works
    @property
    def is_authenticated(self):
        return True

    # This property should return True if this is an active user - in addition to being authenticated,
    # they also have activated their account, not been suspended, or any condition your application
    # has for rejecting an account. Inactive accounts may not log in (without being forced of course).
    # See https://flask-login.readthedocs.io/en/latest/#how-it-works
    @property
    def is_active(self):
        return True

    # This property should return True if this is an anonymous user. (Actual users should return False instead.)
    # See https://flask-login.readthedocs.io/en/latest/#how-it-works
    @property
    def is_anonymous(self):
        return False

    # his method must return a str that uniquely identifies this user, and can be used to load the user
    # from the user_loader callback. Note that this must be a str - if the ID is natively an int or some
    # other type, you will need to convert it to str.
    # See https://flask-login.readthedocs.io/en/latest/#how-it-works
    def get_id(self):
        return str(self.id)

    # Returns true if the plain_text_password matches the (hashed) password in the db
    def correct_password(self, plain_text_password):
        #return bcrypt.check_password_hash(self.password, plain_text_password)
        return sha256(plain_text_password.encode('utf-8')).hexdigest() == self.password


class Product(db.Model):
    __tablename__ = "products"

    # autoincrement is True
    id = db.Column(
        db.Integer(),
        primary_key=True
    )

    name = db.Column(
        db.String(length=30),
        nullable=False
    )

    product_code = db.Column(
        db.String(length=12),
        unique=True
    )

    price = db.Column(
        db.Float(),
        nullable=False
    )

    date_of_withdrawal = db.Column(
        db.DateTime(timezone=False),
        server_default=db.func.current_timestamp()
    )

    # more logical than SellerName. We can find seller name with join
    seller_id = db.Column(
        db.Integer(),
        db.ForeignKey(User.id, ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )

    category = db.Column(
        db.String(length=20),
        nullable=False
    )

    # Relational pattern for the seller of this product (Each product has one seller).
    # Also, for each seller we have a back-reference to its products through User.products
    user_seller = db.relationship(
        User,
        uselist=False,  # One seller explicitly
        back_populates='products'
    )
    """
    # The carts that a product is inside to, using SQL-Alchemy's documentation
    # See https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
    carts = db.relationship(
        'Cart',
        secondary="carts_products",
        back_populates="products",
        cascade="all, delete"
    )
    """

    carts_prods = db.relationship(
        'CartsProductsAssociation',
        back_populates='product'
    )


class Cart(db.Model):
    __tablename__ = "carts"

    # autoincrement is True
    id = db.Column(
        db.Integer(),
        primary_key=True
    )

    user_id = db.Column(
        db.Integer(),
        db.ForeignKey(User.id, ondelete="CASCADE", onupdate="CASCADE"),
        unique=True
    )

    # Relational pattern for the user of this cart. One cart can have only one user. (one-to-one)
    # Also, for each cart we have a back-reference to its owner through User.cart
    user_cart = db.relationship(
        'User',
        uselist=False,
        back_populates="cart"  # One user explicitly
    )
    """
    # The products of a cart using SQL-Alchemy's documentation
    # See https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
    products = db.relationship(
        'Product',
        secondary="carts_products",
        back_populates="carts"
    )
    """
    #cascade="all, delete"  # When a cart is deleted, CASCADE delete tuples in carts_products assoc table

    carts_prods = db.relationship(
        'CartsProductsAssociation',
        back_populates='cart'
    )




