import datetime
import hashlib
import random
import threading
import uuid

from flask import Blueprint

from app import tools

from app.model import db,get_cols, User, EmailCheckCode

from tools import email_tool

user_bp = Blueprint('user', url_prefix='/user', import_name=__name__)


@user_bp.route('/check_code', methods=['GET'])
def get_check_code():
    email = tools.get_arg('email')
    now = str(datetime.datetime.now())
    resp = (db.session.query(EmailCheckCode.check_code)
            .filter(EmailCheckCode.email == email)
            .filter(EmailCheckCode.expired_time >= now)
            .all())
    if resp:
        check_code = resp[0].check_code
    else:
        check_code = str(random.randint(0, 999999))
        check_code = '0' * (6 - len(check_code)) + check_code

        db.session.add(EmailCheckCode(
            email=email,
            check_code=check_code,
            expired_time=str(datetime.datetime.now() + datetime.timedelta(minutes=10)),
        ))
        db.session.commit()
        db.session.close()

    threading.Thread(target=email_tool.send_email, args=['邮箱验证码', check_code, [email]]).start()

    return tools.json_response()


@user_bp.route('/register', methods=['POST'])
def register():
    args = {
        'user_name': tools.get_arg('user_name'),
        'pwd': tools.get_arg('pwd'),
        'email': tools.get_arg('email'),
        'email_check_code': tools.get_arg('email_check_code'),
        'phone': tools.get_arg('phone', necessary=False),
        'pwd_salt': uuid.uuid4().hex,
        'user_id': uuid.uuid4().hex,
    }

    if db.session.query(User.id).filter(User.email==args['email']).all():
        raise tools.ArgsErr(rf'{args["email"]} 已存在')

    now = str(datetime.datetime.now())

    check_code = (db.session.query(EmailCheckCode.check_code)
                  .filter(EmailCheckCode.email == args['email'])
                  .filter(EmailCheckCode.expired_time >= now)
                  .all())
    if not check_code:
        raise tools.ArgsErr(rf'check code expired')

    check_code = check_code[0].check_code
    if check_code != args['email_check_code']:
        raise tools.ArgsErr(rf'check code invalid')

    pwd = hashlib.md5(str(args['pwd']).encode('utf-8')).hexdigest()
    args['pwd'] = hashlib.md5(rf'{pwd}-{args["pwd_salt"]}'.encode('utf-8')).hexdigest()

    args={k:v for k,v in args.items() if k in get_cols(User)}

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
