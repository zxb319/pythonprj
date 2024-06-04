import hashlib
import uuid

from flask import Blueprint

from app import tools

from app.model import db, User

user_bp = Blueprint('user', url_prefix='/user', import_name=__name__)


@user_bp.route('/register', methods=['POST'])
def register():
    args = {
        'user_name': tools.get_arg('user_name'),
        'pwd': tools.get_arg('pwd'),
        'email': tools.get_arg('email', necessary=False),
        'phone': tools.get_arg('phone', necessary=False),
        'pwd_salt': uuid.uuid4().hex,
        'user_id': uuid.uuid4().hex,
    }

    pwd = hashlib.md5(str(args['pwd']).encode('utf-8')).hexdigest()
    args['pwd'] = hashlib.md5(rf'{pwd}-{args["pwd_salt"]}'.encode('utf-8')).hexdigest()

    db.session.add(User(**args))
    db.session.commit()
    return tools.json_response()


@user_bp.route('/login', methods=['POST'])
def login():
    args = {
        'user_name': tools.get_arg('user_name'),
        'pwd': tools.get_arg('pwd'),
    }

    user = (db.session.query(User.user_id, User.pwd, User.pwd_salt)
            .filter(User.user_name == args['user_name']).all())
    if not user:
        raise tools.ArgsErr(rf'用户名不存在')
    user = user[0]

    pwd = hashlib.md5(str(args['pwd']).encode('utf-8')).hexdigest()
    pwd = hashlib.md5(rf'{pwd}-{user.pwd_salt}'.encode('utf-8')).hexdigest()

    if user.pwd == pwd:
        return tools.json_response(data=tools.encode_token(user.user_id))
    else:
        raise tools.LoginErr(rf'用户名或密码不正确')
