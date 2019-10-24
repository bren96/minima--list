from wtforms import Form, StringField, PasswordField, validators, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

class SignupForm(Form):
    """User Sign Up Form."""
    email = StringField('Email',[
        Length(min=6, message=('Little short for an email address?')),
        Email(message=('That\'s not a valid email address.')),
        DataRequired(message=('That\'s not a valid email address.'))])
    password = PasswordField('Password',
        validators=[DataRequired(message="Please enter a password."),])
    confirm = PasswordField('Confirm Password',
        validators=[EqualTo(password, message='Passwords must match.')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        """Email validation."""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class SigninForm(Form):
    """User Sign In Form."""
    email = StringField('Email',[
        Email(message=('That\'s not a valid email address.')),
        DataRequired(message=('That\'s not a valid email address.'))])
    password = PasswordField('Password',
        validators=[DataRequired(message="Please enter a password."),])
    submit = SubmitField('Register')
