from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Required, Regexp

class LoginForm(Form):
    uname = TextField('Uname', validators=[Required(), Regexp(r'\w[_\w]{3,}', message="User name only contain character, number and _ and must greater than 4 characters.")])
    password = PasswordField('Password', validators=[Required()])