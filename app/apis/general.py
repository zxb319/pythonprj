import base64
import json
import math
import os.path
import re
import time

import requests
from flask import Blueprint, Response, send_file, redirect, url_for, make_response, request, jsonify
from sqlalchemy import or_

from app import tools

from app.model import db, Shici
from dsa.html_obj import *

general = Blueprint('general', url_prefix='/', import_name=__name__)


@general.route('/heartbeat', methods=['GET'])
def heartbeat():
    return tools.json_response(data='server running normal!')


@general.route('/', methods=['GET'])
def index():
    return tools.json_response(data={
        k:str(v) for k,v in request.environ.items()
    })


@general.route('/upload_img', methods=['POST'])
def upload_img():
    import uuid
    dir_path = r'D:\weiyun\htmlprj'
    img_fn = rf'{uuid.uuid1().hex}.png'
    file = list(request.files.values())[0]
    file.save(os.path.join(dir_path, img_fn))

    return jsonify({
        "errno": 0,
        "data": {
            "url": rf"/img?fn={img_fn}"
        }
    })


@general.route('/img', methods=['get'])
def get_img():
    dir_path = r'D:\weiyun\htmlprj'
    fn = tools.get_arg('fn')
    return send_file(os.path.join(dir_path, fn))


@general.route('/wang', methods=['get'])
def get_wang():
    return send_file(r'D:\weiyun\htmlprj\index.html')


ROOT_MAP = {
    '微云': rf'd:\weiyun',
    '下载': rf'd:\download',
    'DsC盘': rf'C:\ProgramData',
}


def file_modified_time_str(fp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(fp)))


@general.route('/fs/', methods=['GET'])
def get_fs():
    tb = Table()
    tb.set_head(HeadRow('类型', '文件名', '修改时间'))
    for fn, dir_ in ROOT_MAP.items():
        abs_path = rf'/fs/{fn}'
        tb.append(Row('文件夹' if os.path.isdir(dir_) else '文件', Href(fn, abs_path),
                      file_modified_time_str(dir_)))
    return Response(str(tb))


@general.route('/fs/<root>/', methods=['GET'])
def get_root(root):
    if root not in ROOT_MAP:
        return Response('404 not found', status=404)

    tb = Table()
    tb.set_head(HeadRow('类型', '文件名', '修改时间'))
    tb.append(Row('', Href('返回上一级', '/fs/'), ''))
    for fn in os.listdir(ROOT_MAP[root]):
        abs_path = rf'/fs/{root}/{fn}'
        fp = os.path.join(ROOT_MAP[root], fn)
        type_ = '文件夹' if os.path.isdir(fp) else '文件'
        tb.append(Row(type_, Href(fn, abs_path), file_modified_time_str(fp)))

    return Response(str(tb))


@general.route('/fs/<root>/<path:p>', methods=['GET'])
def get_dir(root, p):
    if root not in ROOT_MAP:
        return Response('404 not found', status=404)

    p = tuple(x for x in p.split('/') if x)
    fp = os.path.join(ROOT_MAP[root], *p)
    if not os.path.exists(fp):
        return Response('404 not found', status=404)
    elif os.path.isdir(fp):
        tb = Table()
        tb.set_head(HeadRow('类型', '文件名', '修改时间'))
        tb.append(Row('', Href('返回上一级', rf'/fs/{root}/{"/".join(p[:-1])}'), ''))
        for fn in os.listdir(fp):
            abs_path = rf'/fs/{root}/{"/".join(p)}/{fn}'
            sub_fp = os.path.join(fp, fn)
            type_ = '文件夹' if os.path.isdir(sub_fp) else '文件'
            # type_, rf'<a href="{abs_path}">{fn}</a>', file_modified_time_str(sub_fp)
            tb.append(Row(type_, Href(fn, abs_path), file_modified_time_str(sub_fp)))
        return Response(str(tb))
    else:
        # with open(fp,'rb') as f:
        #     content=f.read()
        # resp=Response(content,content_type=None)
        # resp.headers['Content-Disposition']=rf'attachment; filename={p[-1]}'
        # return resp
        resp = send_file(fp)
        return resp
