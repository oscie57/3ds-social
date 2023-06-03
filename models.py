from flask_sqlalchemy import BaseQuery, SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.event import listens_for


db = SQLAlchemy()
login = LoginManager()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@listens_for(User.__table__, "after_create")
def create_default_user(target, connection, **kw):
    """Adds a default user to The Underground.
    By default, we assume admin:admin."""
    table = User.__table__
    connection.execute(
        table.insert().values(
            username="admin",
            password_hash=generate_password_hash("admin")
        )
    )