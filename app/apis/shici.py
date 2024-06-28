from flask import Blueprint, Response, send_file, redirect, url_for, make_response
from sqlalchemy import or_

from app import tools

from app.model import db, Shici
from dsa.html_obj import *

shici_bp = Blueprint('shici', url_prefix='/shici', import_name=__name__)


@shici_bp.route('/shicis', methods=['GET'])
@tools.check_login
def get_shicis():
    cur_page, page_size = tools.get_page_info()
    key_word = tools.get_arg('key_word', necessary=False)
    query = db.session.query(Shici.id, Shici.title, Shici.author, Shici.chaodai, Shici.content)

    if key_word:
        query = query.filter(or_(Shici.title.like(f'%{key_word}%'), Shici.author.like(f'%{key_word}%'),
                                 Shici.content.like(f'%{key_word}%')))
    else:
        key_word = ''
    res = query.offset((cur_page - 1) * page_size).limit(page_size).all()

    res = [tools.row_object_to_dict(x) for x in res]
    return tools.json_response(data=res)


@shici_bp.route('/shici', methods=['GET'])
@tools.check_login
def get_shici():
    id = tools.get_arg('id')
    res = db.session.query(Shici.id, Shici.title, Shici.author, Shici.chaodai, Shici.content).filter(
        Shici.id == id).all()
    if not res:
        raise tools.ArgsErr(rf'id={id}的数据不存在')

    return tools.json_response(data=tools.row_object_to_dict(res[0]))


@shici_bp.route('/shici', methods=['POST'])
@tools.check_login
def post_shici():
    args = {
        'title': tools.get_arg('title'),
        'author': tools.get_arg('author'),
        'chaodai': tools.get_arg('chaodai'),
        'content': tools.get_arg('content'),
    }
    db.session.add(Shici(**args))
    db.session.commit()
    db.session.close()

    return tools.json_response()


@shici_bp.route('/shici', methods=['PUT'])
@tools.check_login
def put_shici():
    args = {
        'id': tools.get_arg('id'),
        'title': tools.get_arg('title'),
        'author': tools.get_arg('author'),
        'chaodai': tools.get_arg('chaodai'),
        'content': tools.get_arg('content'),
    }
    db.session.query(Shici).filter(Shici.id == args['id']).update(args)
    db.session.commit()
    db.session.close()

    return tools.json_response()


@shici_bp.route('/shici', methods=['DELETE'])
@tools.check_login
def delete_shici():
    args = {
        'id': tools.get_arg('id'),
    }
    db.session.query(Shici).filter(Shici.id == args['id']).delete()
    db.session.commit()
    db.session.close()

    return tools.json_response()
