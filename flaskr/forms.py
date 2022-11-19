from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, DateField, DateTimeLocalField
from wtforms.validators import Length, EqualTo, Email, InputRequired, ValidationError, Optional
from flaskr.models import User


class RegisterForm(FlaskForm):
    """ Form to register a new user. """

    # Magic function from FlaskForm validate_<field_name>
    # See https://wtforms.readthedocs.io/en/3.0.x/validators/
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).one_or_none()
        if user:  # username exists in database
            raise ValidationError("Username already exists! Please try a different username")

    # Magic function from FlaskForm validate_<field_name>
    # See https://wtforms.readthedocs.io/en/3.0.x/validators/
    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).one_or_none()
        if user:  # email exists in database
            raise ValidationError("E-mail already exists! Please try a different e-mail address!")

    name = StringField(
        label="Name:",
        validators=[
            InputRequired(),
            Length(min=2, max=30)
        ]
    )

    surname = StringField(
        label="Surname:",
        validators=[
            InputRequired(),
            Length(min=2, max=30)
        ]
    )

    username = StringField(
        label="Username:",
        validators=[
            InputRequired(),
            Length(min=3, max=30)
        ]
    )

    email = StringField(
        label="Email Address:",
        validators=[
            InputRequired(),
            Email()
        ]
    )

    password1 = PasswordField(
        label="Password:",
        validators=[
            InputRequired(),
            Length(min=3, max=60)
        ]
    )

    password2 = PasswordField(
        label="Confirm Password:",
        validators=[
            EqualTo('password1')
        ]
    )

    role = SelectField(
        label="Role:",
        choices=["USER", "PRODUCTSELLER"]
    )

    submit = SubmitField(
        label="Create Account"
    )


class LoginForm(FlaskForm):
    """ Form to register a new user. """

    username = StringField(
        label="Username:",
        validators=[
            InputRequired(),
            Length(min=3, max=30)
        ]
    )

    password = PasswordField(
        label="Password:",
        validators=[
            InputRequired(),
            Length(min=3, max=60)
        ]
    )

    submit = SubmitField(
        label="Sign In"
    )


class UpdateUserForm(FlaskForm):
    name = StringField(
        label="Name:",
        validators=[
            InputRequired(),
            Length(min=2, max=30)
        ]
    )

    surname = StringField(
        label="Surname:",
        validators=[
            InputRequired(),
            Length(min=2, max=30)
        ]
    )

    username = StringField(
        label="Username:",
        validators=[
            InputRequired(),
            Length(min=3, max=30)
        ]
    )

    email = StringField(
        label="Email Address:",
        validators=[
            InputRequired(),
            Email()
        ]
    )

    role = SelectField(
        label="Role:",
        choices=["USER", "PRODUCTSELLER", "ADMIN"]
    )

    submit = SubmitField(
        label="Submit"
    )

    cancel = SubmitField(
        label="Cancel",
        render_kw={'formnovalidate': True}
    )


class ProductForm(FlaskForm):
    """ Form to create a new product. """

    name = StringField(
        label="Name:",
        validators=[
            InputRequired(),
            Length(min=2, max=30)
        ]
    )

    price = FloatField(
        label="Price:",
        validators=[
            InputRequired()
        ]
    )

    category = StringField(
        label="Category:",
        validators=[
            InputRequired(),
            Length(min=2, max=30)
        ]
    )

    date_of_withdrawal = DateTimeLocalField(
        label="Date/Time of Withdrawal",
        format='%Y-%m-%dT%H:%M',
        validators=[
            InputRequired()
        ]
    )

    submit = SubmitField(
        label="Confirm"
    )

    cancel = SubmitField(
        label="Cancel",
        render_kw={'formnovalidate': True}
    )


class SearchProductForm(FlaskForm):
    """ Form for searching products. """

    product_name = StringField(
        label="Product Name:",
        validators=[
            Optional()  # If empty then None
        ]
    )

    category = StringField(
        label="Category:",
        validators=[
            Optional()  # If empty then None
        ]
    )

    lowest_price = FloatField(
        label="Greater (price) than:",
        validators=[
            Optional()  # If empty then None
        ]
    )

    highest_price = FloatField(
        label="Lower (price) than:",
        validators=[
            Optional()  # If empty then None
        ]
    )

    after_than_date = DateField(
        label="After than:",
        validators=[
            Optional()  # If empty then None
        ]
    )

    before_than_date = DateField(
        label="Before than:",
        validators=[
            Optional()  # If empty then None
        ]
    )

    seller_name = StringField(
        label="Seller Name:",
        validators=[
            Optional()  # If empty then None
        ]
    )

    seller_surname = StringField(
        label="Seller Surname:",
        validators=[
            Optional()  # If empty then None
        ]
    )

    submit = SubmitField(
        label="Search",
        validators=[
            Optional()  # If empty then None
        ]
    )

