import getpass
import json
import re
import time

import requests


def get_work_time_details(user_id, user_password, month):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71',

    }
    data = {
        'userName': user_id,
        'j_username': user_id,
        'password': user_password,
        'j_password': user_password,
    }
    res = session.post("http://ics.chinasoftinc.com/r1portal/login", allow_redirects=True, data=data, headers=headers)

    url = re.search(r'\'([^\']+)\'', res.text).group(1)

    res = session.get(url, headers=headers)

    headers['Referer'] = url
    headers['ROLTPAToken'] = session.cookies.get('ROLTPAToken')
    headers['Content-Type'] = 'application/json;charset=UTF-8'
    headers['Host'] = 'ics.chinasoftinc.com'
    headers['Origin'] = 'http://ics.chinasoftinc.com'
    headers['X-Requested-With'] = 'XMLHttpRequest'

    url = 'http://ics.chinasoftinc.com/elp/getUserProtocol'
    data = {"tacticsStatus": 2}
    res = session.post(url=url, json=data, headers=headers, cookies=session.cookies)

    url = 'http://ics.chinasoftinc.com:8010/sso/toLoginYellow'
    res = session.get(url=url, headers=headers, cookies=session.cookies, allow_redirects=False)

    url = res.headers.get('Location')
    empCode = re.search(r'empCode=(.+)$', res.headers.get('Location')).group(1)

    res = session.get(url, headers=headers, cookies=session.cookies)

    headers['Referer'] = url

    res = session.post(url='http://ics.chinasoftinc.com:8010/ehr_saas/web/user/loginByEmpCode.jhtml',
                       json={'empCode': empCode}, headers=headers, cookies=session.cookies)

    res = json.loads(res.text)
    token = res.get('result').get('data').get('token')

    url = 'http://ics.chinasoftinc.com:8010/ehr_saas/web/icssAttEmpDetail/getLocSetDataByPage.empweb'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['token'] = token
    data = f'pageIndex=1&pageSize=100&search=%7B%22dt%22%3A%22{month}%22%7D'
    res = session.post(url=url, data=data, headers=headers)

    res = json.loads(res.text)
    records = res.get('result').get('data').get('page').get('items')
    return records


format_str = '%Y-%m-%d %H:%M:%S'


def work_time(from_time: str, to_time: str):
    if from_time == to_time:
        return 0
    from_t = from_time[-8:]
    to_t = to_time[-8:]
    t0800 = '08:00:00'
    t1200 = '12:00:00'
    t1330 = '13:30:00'
    t1730 = '17:30:00'
    t1800 = '18:00:00'

    if from_t <= t0800:
        from_t = t0800
    elif t1200 <= from_t <= t1330:
        from_t = t1330
    elif t1730 <= from_t <= t1800:
        from_t = t1800

    if to_t <= t0800:
        to_t = t0800
    elif t1200 <= to_t <= t1330:
        to_t = t1200
    elif t1730 <= to_t <= t1800:
        to_t = t1730

    if from_t >= to_t:
        return 0

    rest_hour = 0
    if from_t <= t1200 and t1330 <= to_t <= t1730:
        rest_hour = 1.5
    elif from_t <= t1200 and to_t >= t1800:
        rest_hour = 2
    elif t1330 <= from_t <= t1730 and to_t >= t1800:
        rest_hour = 0.5

    from_time = from_time[:-8] + from_t
    to_time = to_time[:-8] + to_t
    from_time = time.mktime(time.strptime(from_time, format_str))
    to_time = time.mktime(time.strptime(to_time, format_str))

    return (to_time - from_time) / 3600 - rest_hour


def compute(id, pwd, month):
    records = get_work_time_details(id, pwd, month=month)

    data = {}
    today = time.strftime('%Y-%m-%d', time.localtime())
    for r in records:
        if r['dt'] not in data:
            data[r['dt']] = []
        data[r['dt']].append(r['checktime'])
    daily_work_times = {k: work_time(min(v), max(v)) for k, v in data.items() if not (k == today and len(v) == 1)}
    total_work_time = sum(v for k, v in daily_work_times.items())
    days_count = len(daily_work_times)
    average_work_time = total_work_time / days_count
    lack_time = days_count * 8 - total_work_time

    print('*'*60)
    print(f'{month}的数据：')
    print('总工时: ', total_work_time)
    print('平均工时: ', average_work_time)
    if lack_time < 0:
        print(f'超出标准工时: {-lack_time}小时,即{-lack_time * 60}分')
    else:
        print(f'缺工时: {lack_time}小时,即{lack_time * 60}分')

    lack_time += days_count * 0.5
    if lack_time > 0:
        print(f'平均工时要达到8.5，缺工时: {lack_time}小时,即{lack_time * 60}分')
    else:
        print(f'已满足8.5，且超过: {-lack_time}小时,即{-lack_time * 60}分')
    print('*' * 60)


if __name__ == '__main__':
    import mima
    id = mima.id
    pwd = mima.pwd
    if not id:
        id = input('请输入中软工号：')
    if not pwd:
        pwd = getpass.getpass('请输入密码：')
    month = input('请输入月份(格式YYYY-MM,不输入的话，默认当前月)：')
    if not month:
        month = time.strftime('%Y-%m', time.localtime())
    compute(id, pwd, month)
    input('按enter键结束...')
