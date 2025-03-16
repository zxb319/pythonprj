import os
import threading
import time

import waitress as waitress
from flask import Flask
from flask_cors import CORS
from app.model import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = rf'mysql+pymysql://root:zxb319@localhost/shici'
    db.init_app(app)
    CORS(app)
    return app


def main():
    app = create_app()
    from app.apis.general import general
    app.register_blueprint(general)

    from app.apis.user import user_bp
    app.register_blueprint(user_bp)

    from app.apis.shici import shici_bp
    app.register_blueprint(shici_bp)

    from app import tools

    tools.register_before_handle(app)
    tools.register_err_handles(app)
    # threading.Thread(target=lambda :os.system('wssh -port=9999')).start()
    print('服务已启动')
    waitress.serve(app, port=55555)


if __name__ == '__main__':
    threading.Thread(target=main).start()
    time.sleep(1)
    import webbrowser

    webbrowser.open('http://localhost:55555/fs')
