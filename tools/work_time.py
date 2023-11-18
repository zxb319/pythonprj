import base64
import datetime
import getpass
import json
import os.path
import random
import re
import time
import urllib.parse

import requests
requests.packages.urllib3.disable_warnings()

import Crypto.Random

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def generate_aes_key(size=16):
    a = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    r = [a[random.Random().randint(0, len(a) - 1)] for i in range(size)]
    return ''.join(r).encode('utf-8')


def aes_encrypt(msg, key):
    aes = AES.new(key, AES.MODE_ECB)
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    # msg=base64.b64encode(msg)
    padded_msg = pad(msg, AES.block_size)
    r = aes.encrypt(padded_msg)
    return base64.b64encode(r).decode('utf-8')


def rsa_encrypt(msg, pub_key):
    pub_key = rf'''-----BEGIN RSA PUBLIC KEY-----
{pub_key}
-----END RSA PUBLIC KEY-----'''
    pub_key = RSA.import_key(pub_key)
    rsa = PKCS1_v1_5.new(pub_key)
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    encrypted = rsa.encrypt(msg)
    encrypted = base64.b64encode(encrypted).decode('utf-8')
    return encrypted


except_holidays = {
    '2022-09-12', '2022-10-03', '2022-10-04', '2022-10-05', '2022-10-06', '2022-10-07',
    '2023-01-02', '2023-01-23', '2023-01-24', '2023-01-25', '2023-01-26', '2023-01-27',
    '2023-04-05',
    '2023-05-01', '2023-05-02', '2023-05-03',
    '2023-06-22', '2023-06-23',
    '2023-09-29',
    '2023-10-02', '2023-10-03', '2023-10-04', '2023-10-05', '2023-10-06',
}

except_workdays = {
    '2022-10-08', '2022-10-09',
    '2023-01-28', '2023-01-29',
    '2023-04-23',
    '2023-05-06',
    '2023-06-25',
    '2023-10-07', '2023-10-08',
}

date_format_str = '%Y-%m-%d'


def is_workday(d):
    return datetime.datetime.strptime(d, date_format_str).weekday() in (0, 1, 2, 3, 4) and d not in except_holidays or d in except_workdays


def get_token(user_id, user_password):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71',
    }

    url = rf'https://ics.chinasoftinc.com/r1portal/getPublicKey'
    resp = session.get(url, headers=headers, verify=False, allow_redirects=False)
    res = json.loads(resp.text)
    rsaPublicKey = res['data']['rsaPublicKey']

    aes_key = generate_aes_key(16)
    # print(aes_key)
    # print(rsaPublicKey)
    # print(user_id)
    # print(user_password)
    aes_encrypted_user_id = aes_encrypt(user_id, aes_key)
    aes_encrypted_user_pwd = aes_encrypt(user_password, aes_key)
    rsa_encrypted_aes_key = rsa_encrypt(aes_key, rsaPublicKey)

    data = {
        'encryptKey': 'pteZF5GTC5qsvV513%2FTCuh9sPy3wWme990d6udH5zrehN4bcvWHHmrj0UtidgbEsRbvM2zgsyS9TOEB21y7ahETpk0h0o1W%2F4Q2tBcBYu8A76aabeRx82kCUt7J4aTz1fxOx088PYTorCpOXh%2FkDZIFN3gbFWsytphm835E6HqI%3D',
        'headAgreement': 'https',
        'linkpage': '',
        'userName': 'lUGQg3J%2B2K5pJgZAIN72ow%3D%3D',
        'password': 'YjyIrz9OLv8CLeny2AMYVg%3D%3D',
    }
    data = {
        'encryptKey': urllib.parse.quote(rsa_encrypted_aes_key),
        'headAgreement': 'https',
        'linkpage': '',
        'userName': urllib.parse.quote(aes_encrypted_user_id),
        'password': urllib.parse.quote(aes_encrypted_user_pwd),
    }

    res = session.post("https://ics.chinasoftinc.com/r1portal/login", allow_redirects=True, data=data, headers=headers)

    url = re.search(r'\'([^\']+)\'', res.text).group(1)

    res = session.get(url, headers=headers)

    headers['Referer'] = url
    headers['ROLTPAToken'] = session.cookies.get('ROLTPAToken')
    headers['Content-Type'] = 'application/json;charset=UTF-8'
    headers['Host'] = 'ics.chinasoftinc.com'
    headers['Origin'] = 'https://ics.chinasoftinc.com'
    headers['X-Requested-With'] = 'XMLHttpRequest'

    url = 'https://ics.chinasoftinc.com/elp/getUserProtocol'
    data = {"tacticsStatus": 2}
    res = session.post(url=url, json=data, headers=headers, cookies=session.cookies)

    url = 'https://yihr.chinasoftinc.com:18010/sso/toLogin'
    res = session.get(url=url, headers=headers, cookies=session.cookies, allow_redirects=False, verify=False)

    url = res.headers.get('Location')

    empCode = re.search(r'empCode=(.+)$', res.headers.get('Location')).group(1)

    res = session.get(url, headers=headers, cookies=session.cookies)

    headers['Referer'] = url

    res = session.post(url='https://yihr.chinasoftinc.com:18010/ehr_saas/web/user/loginByEmpCode.jhtml',
                       json={'empCode': empCode}, headers=headers, cookies=session.cookies, verify=False)
    res = json.loads(res.text)
    token = res.get('result').get('data').get('token')

    headers['token'] = token
    return session, headers


def get_work_time_details(session, headers, months):
    url = 'https://yihr.chinasoftinc.com:18010/ehr_saas/web/icssAttEmpDetail/getLocSetDataByPage.empweb'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    months_records = {}
    for month in months:
        data = f'pageIndex=1&pageSize=100&search=%7B%22dt%22%3A%22{month}%22%7D'
        res = session.post(url=url, data=data, headers=headers, verify=False)
        res = json.loads(res.text)
        records = res.get('result').get('data').get('page').get('items')
        months_records[month] = records

    return months_records


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


def round_(num: float):
    if num is None:
        return None
    return round(num, 4)


def compute_plan_work_times(plan_work_time: float, daily_work_times: dict, today, all_workdays):
    plan_work_times = {k: v for k, v in daily_work_times.items()}
    for d in all_workdays:
        if d not in plan_work_times and d > today:
            plan_work_times[d] = plan_work_time
    print(f'如果以后工作{"%4.1f" % plan_work_time}小时，平均工时为：{round_(sum(plan_work_times.values()) / len(plan_work_times))}')


def compute(records):
    if len(records) == 0:
        print('没有数据')
        return
    data = {}
    today = time.strftime('%Y-%m-%d', time.localtime())
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    for r in records:
        if r['dt'] not in data:
            data[r['dt']] = []
        data[r['dt']].append(r['checktime'])
    daily_work_times = {k: work_time(min(v), max(v)) for k, v in data.items()}
    daily_work_times = {k: v for k, v in daily_work_times.items() if v >= 7 and is_workday(k)}
    total_work_time = sum(v for k, v in daily_work_times.items())
    days_count = len(daily_work_times)
    average_work_time = (total_work_time / days_count) if days_count else None
    lack_time = days_count * 8 - total_work_time

    print('*' * 35)
    cur_month = records[0]["dt"][:7]
    print(f'{cur_month}的数据：')
    print(f'出勤天数：{days_count}')
    print('总工时: ', round_(total_work_time), '小时')
    print('平均工时: ', round_(average_work_time), '小时')
    if lack_time < 0:
        print(f'超出标准工时: {round_(-lack_time)} 小时,即 {round_(-lack_time * 60)} 分')
    else:
        print(f'缺工时: {round_(lack_time)} 小时,即 {round_(lack_time * 60)} 分')

    lack_time += days_count * 0.5
    if lack_time > 0:
        print(f'要达到8.5，缺工时: {round_(lack_time)} 小时,即 {round_(lack_time * 60)} 分')
    else:
        print(f'已满足8.5，且超过: {round_(-lack_time)} 小时,即 {round_(-lack_time * 60)} 分')

    first_day = datetime.date(int(cur_month[:4]), int(cur_month[-2:]), 1)
    all_workdays = {str(d) for d in (first_day + datetime.timedelta(days=i) for i in range(31)) if
                    is_workday(str(d)) and d.month == int(cur_month[-2:])}
    exception_data = [(k, v) for k, v in data.items() if min(v)[-8:] > '09:00:00' or max(v)[-8:] < '17:30:00' and today != k]
    exception_data += [(d, []) for d in all_workdays if d <= today and d not in data]
    if len(exception_data) > 0:
        print(f'异常打卡：')
        for ed in sorted(exception_data):
            print(ed[0], [x[-8:] for x in ed[1]])

    print(f'打卡记录：')
    for k, v in data.items():
        print(k, '\t'.join([x[-8:] for x in v]), round_(daily_work_times.get(k)), sep='\t')

    if today in all_workdays and today not in daily_work_times:
        from_time = min(data.get(today, [today + ' 08:30:00']))
        to_time = today + ' 17:30:00'
        if to_time < now:
            to_time = now
        daily_work_times[today] = work_time(from_time, to_time)
        print(f'\n如果{to_time[11:]}下班，平均工时：{round_(sum(v for v in daily_work_times.values()) / len(daily_work_times))}')
    print()
    compute_plan_work_times(7, daily_work_times, today, all_workdays)
    compute_plan_work_times(7+1/12, daily_work_times, today, all_workdays)
    compute_plan_work_times(7.5, daily_work_times, today, all_workdays)
    compute_plan_work_times(8, daily_work_times, today, all_workdays)
    compute_plan_work_times(8.5, daily_work_times, today, all_workdays)
    compute_plan_work_times(9, daily_work_times, today, all_workdays)
    compute_plan_work_times(9.5, daily_work_times, today, all_workdays)
    compute_plan_work_times(10, daily_work_times, today, all_workdays)

    print('*' * 35)


def format_month(m, regexes):
    for reg, func in regexes.items():
        if re.search(reg, m):
            return func(m)


def save_info(id_or_pwd, val):
    fp = os.path.abspath(__file__)
    regex = rf'^\s*{id_or_pwd}\s*=\s*\'[^\']*\'\s*$'

    with open(fp, 'r', encoding='utf8') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        if re.search(regex, lines[i]):
            lines[i] = re.search(r'^\s*', lines[i]).group(0) + f'{id_or_pwd} = \'{val}\'\n'

    with open(fp, 'w', encoding='utf8') as f:
        f.writelines(lines)


if __name__ == '__main__':
    id = '335524'
    pwd = 'gbbscsyrrd319!'

    if not id:
        id = input('初次使用，请输入中软工号(脚本里会记住账号)：')
        save_info('id', id)
    if not pwd:
        pwd = getpass.getpass('初次使用，请输入密码(脚本里会记住密码)：')
        save_info('pwd', pwd)

    print(f'当前账号{id}')

    session, headers = get_token(id, pwd)

    while True:
        month = input('请输入月份(格式支持：{YYYY-MM YYYY-M YY-MM YY-M MM M},不输入默认当月)：')
        if month:
            year = datetime.datetime.now().year
            regexes = {
                r'^[0-9]{4}-1[0-2]$': lambda m: m,
                r'^[0-9]{4}-0[1-9]$': lambda m: m,
                r'^[0-9]{4}-[1-9]$': lambda m: f'{m[:4]}-0{m[-1:]}',

                r'^[0-9]{2}-1[0-2]$': lambda m: f'{year // 100}{m}',
                r'^[0-9]{2}-0[1-9]$': lambda m: f'{year // 100}{m}',
                r'^[0-9]{2}-[1-9]$': lambda m: f'{year // 100}{m[:2]}-0{m[-1:]}',

                r'^[0-9]{4}1[0-2]$': lambda m: f'{m[:4]}-{m[-2:]}',
                r'^[0-9]{4}0[1-9]$': lambda m: f'{m[:4]}-{m[-2:]}',

                r'^1[0-2]$': lambda m: f'{year}-{m}',
                r'^0[1-9]$': lambda m: f'{year}-{m}',
                r'^[1-9]$': lambda m: f'{year}-0{m}',
            }
            months = re.split(r'[^0-9\-]+', month)
            months = {x for x in (format_month(m, regexes) for m in months) if x}
            if not months:
                print(f'输入的月份不对！')
        else:
            today = time.localtime()
            month = time.strftime('%Y-%m', today)
            months = {month}

        try:
            months_records = get_work_time_details(session, headers, months)
        except Exception as e:
            session, headers = get_token(id, pwd)
            print(f'上次登录已过时，已重新登录。')
            months_records = get_work_time_details(session, headers, months)

        for _, records in months_records.items():
            compute(records)

        break

    # input('按enter键结束...')
