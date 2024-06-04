from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
