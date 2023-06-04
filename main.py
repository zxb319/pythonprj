import waitress as waitress
from flask import Flask
from app.model import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']=rf'mysql+pymysql://root:zxb319@localhost/shici'
    db.init_app(app)
    return app



if __name__ == '__main__':
    from app.apis.general import general
    app = create_app()
    app.register_blueprint(general)
    from app import tools
    tools.register_before_handle(app)
    tools.register_err_handles(app)
    print('服务已启动')
    waitress.serve(app, port=8888)
