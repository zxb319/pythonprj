from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_cols(model:db.Model):
    return set(x for x in model.__dict__ if not x.startswith('_') and x!='id')

class ErrorLog(db.Model):
    __tablename__ = 'error_log'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    create_time = db.Column(db.String(20))
    content = db.Column(db.Text)


class Shici(db.Model):
    __tablename__ = 'shici'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    url_code = db.Column(db.BigInteger, unique=True)
    author = db.Column(db.String(100))
    chaodai = db.Column(db.String(100))
    title = db.Column(db.String(100))
    content = db.Column(db.Text)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(32))
    user_name = db.Column(db.String(32))
    pwd = db.Column(db.String(32))
    pwd_salt = db.Column(db.String(32))
    email = db.Column(db.String(32))
    phone = db.Column(db.String(32))


class EmailCheckCode(db.Model):
    __tablename__ = 'email_check_code'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    email = db.Column(db.String(32))
    check_code = db.Column(db.String(32))
    expired_time = db.Column(db.String(32))


