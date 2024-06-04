import os
import threading

import waitress as waitress
from flask import Flask
from app.model import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = rf'mysql+pymysql://root:zxb319@localhost/shici'
    db.init_app(app)
    return app


if __name__ == '__main__':

    app = create_app()
    from app.apis.general import general
    app.register_blueprint(general)

    from app.apis.user import user_bp
    app.register_blueprint(user_bp)

    from app import tools

    tools.register_before_handle(app)
    tools.register_err_handles(app)
    # threading.Thread(target=lambda :os.system('wssh -port=9999')).start()
    print('服务已启动')
    waitress.serve(app, port=8888)
