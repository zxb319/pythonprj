import math
import os.path
import time

from flask import Blueprint, Response, send_file
from sqlalchemy import or_

from app import tools

from app.model import db, Shici
from dsa.html import *

general = Blueprint('general', url_prefix='/', import_name=__name__)


@general.route('/heartbeat', methods=['GET'])
def heartbeat():
    return tools.json_response(data='server running normal!')


@general.route('/shicis/', methods=['GET'])
def get_shicis():
    cur_page, page_size = tools.get_page_info()
    key_word = tools.get_arg('key_word', necessary=False)
    query = db.session.query(Shici.id, Shici.title, Shici.author, Shici.chaodai, Shici.content)

    if key_word:
        query = query.filter(or_(Shici.title.like(f'%{key_word}%'), Shici.author.like(f'%{key_word}%'), Shici.content.like(f'%{key_word}%')))
    else:
        key_word = ''
    res = query.offset((cur_page - 1) * page_size).limit(page_size).all()

    ht = Html(title='诗词列表')
    form = Form('/shicis/', method='GET')
    parts = [
        Row(Label('页码：'), FormText('cur_page', 1)),
        Row(Label('每页：'), FormText('page_size', page_size)),
        Row(Label('关键词：'), FormText('key_word', key_word if key_word else '')),
        Row(FormSubmit('搜索')),
    ]
    for p in parts:
        form.append(p)
    ht.append(form)

    tb = Table(head=HeadRow('ID', '标题', '作者', '朝代', '内容'))
    for r in res:
        r = tools.row_object_to_dict(r)
        abs_count = 70
        abs_content = r['content'][:abs_count] + ('...' if len(r['content']) > abs_count else '')
        row = Row(Href(r['id'], rf'/shici/?id={r["id"]}'), r['title'], r['author'], r['chaodai'], abs_content)
        tb.append(row)

    ht.append(tb)

    total = query.count()
    page_count = math.ceil(total / page_size)
    tb = Table()
    last = Href('上一页', f'/shicis/?cur_page={cur_page - 1}&page_size={page_size}&key_word={key_word}') if cur_page > 1 else ''
    next = Href('下一页', f'/shicis/?cur_page={cur_page + 1}&page_size={page_size}&key_word={key_word}') if cur_page < page_count else ''
    tb.append(Row(last, next, rf'共{page_count}页{total}条'))
    ht.append(tb)
    return Response(str(ht))


@general.route('/shici/', methods=['GET'])
def get_shici():
    id = tools.get_arg('id')
    res = db.session.query(Shici.id, Shici.title, Shici.author, Shici.chaodai, Shici.content).filter(Shici.id == id).all()
    if not res:
        return Response(rf'id={id}的数据不存在！', status=404)
    tb = Table()
    tb.set_head(HeadRow(res[0].title))
    tb.append(Row(res[0].author))
    tb.append(Row(res[0].chaodai))
    lines = res[0].content.split('。')
    contents = []
    for l in lines:
        if not l:
            continue
        contents.append(rf'{l}。')
    for c in contents:
        tb.append(Row(c))
    return Response(str(tb))


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
        tb.append(Row('文件夹' if os.path.isdir(dir_) else '文件', Href(fn, abs_path), file_modified_time_str(dir_)))
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
