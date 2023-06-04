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


def create_table():
    db.create_all(bind_key=None)


if __name__ == '__main__':
    create_table()
