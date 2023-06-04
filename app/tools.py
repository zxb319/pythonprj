import time
import traceback

from flask import jsonify, request, Flask
from app.model import db, ErrorLog


def row_object_to_dict(o):
    # print(o.__dict__)
    for k in o.__dir__():
        if k == '_mapping':
            return dict(getattr(o, k))


class RespCode:
    SUCCESS = 0
    ARGSERR = 1
    LOGINERR = 2
    PERMITERR = 3
    SERVERERR = 4


class ArgsErr(Exception):
    pass


class LoginErr(Exception):
    pass


class PermitErr(Exception):
    pass


def json_response(data=None, resp_code=RespCode.SUCCESS, msg='SUCCESS'):
    return jsonify({
        'data': data,
        'ret_code': resp_code,
        'msg': msg,
        'cost_time': time.time() - request.start_time
    })


def register_before_handle(app: Flask):
    @app.before_request
    def func():
        request.start_time = time.time()
        content_type = request.content_type
        if content_type:
            content_type = content_type.lower()
        else:
            content_type = ''

        request.all_args = {}

        if request.args:
            request.all_args.update(request.args)

        if 'json' in content_type:
            if type(request.json) is dict:
                request.all_args.update(request.json)
        elif 'x-www-form-urlencoded' in content_type:
            request.all_args.update(request.form)
        elif 'form-data' in content_type:
            request.all_args.update(request.files)
            request.all_args.update(request.form)

        # print(request.all_args)


def get_arg(arg_name, necessary=True, types={str, int, float}, legal_func=lambda x: True):
    res = request.all_args.get(arg_name)
    if necessary and (res is None or res == ''):
        raise ArgsErr(rf'{arg_name} required!')
    if res and type(res) not in types:
        raise ArgsErr(rf'{arg_name}: expect {types} but get {type(res)}')
    if res and not legal_func(res):
        raise ArgsErr(rf'{arg_name}={res} is not legal!')
    return res


def get_page_info():
    cur_page = get_arg('cur_page', types={int, str}, legal_func=lambda x: str(x).isdecimal() and int(x) > 0)
    page_size = get_arg('page_size', types={int, str}, legal_func=lambda x: str(x).isdecimal() and int(x) > 0)

    cur_page = int(cur_page)
    page_size = int(page_size)
    return cur_page, page_size


def now_str():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def log(*msgs, sep=' '):
    db.session.add(ErrorLog(create_time=now_str(), content=sep.join(str(x) for x in msgs)))
    db.session.commit()


def _500_handle_func(e):
    log(traceback.format_exc())
    return json_response(resp_code=RespCode.SERVERERR, msg=str(e))


_err_handle_map = {
    ArgsErr: lambda e: json_response(resp_code=RespCode.ARGSERR, msg=str(e)),
    LoginErr: lambda e: json_response(resp_code=RespCode.LOGINERR, msg=str(e)),
    PermitErr: lambda e: json_response(resp_code=RespCode.PERMITERR, msg=str(e)),
    500: _500_handle_func
}


def register_err_handles(app: Flask):
    for e, h in _err_handle_map.items():
        app.register_error_handler(e, h)
