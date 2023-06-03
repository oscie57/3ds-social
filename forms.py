from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired

from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    FileField,
    SelectField,
    TextAreaField,
    BooleanField,
    IntegerField
)
from wtforms.validators import DataRequired, Length, ValidationError


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Login!")

class NewUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password1 = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])

    upload = SubmitField("Complete")

    def validate_password1(self, _):
        print(self.password1.data + "-" + self.password2.data)
        if self.password1.data != self.password2.data:
            return ValidationError("New passwords must be the same.")
        
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password1 = PasswordField("New Password", validators=[DataRequired()])
    new_password2 = PasswordField("Confirm New Password", validators=[DataRequired()])
    complete = SubmitField("Complete")

    def validate_current_password(self, _):
        if self.current_password.data == self.new_password1.data:
            return ValidationError("New password cannot be the same as current!")
        
    def validate_new_password(self, _):
        if self.new_password1.data != self.new_password2.data:
            return ValidationError("New passwords must be the same.")