import datetime
import math
import time

date_format = '%Y-%m-%d'

datetime_format = f'{date_format} %H:%M:%S'

# 阴历每月只能是29或30天，一年用12（或13）个二进制位表示，对应位为1表30天，否则为29天
_lunar_months_day_count = [
    0x4ae0, 0xa570, 0x5268, 0xd260, 0xd950, 0x6aa8, 0x56a0, 0x9ad0, 0x4ae8, 0x4ae0,  # 1910
    0xa4d8, 0xa4d0, 0xd250, 0xd548, 0xb550, 0x56a0, 0x96d0, 0x95b0, 0x49b8, 0x49b0,  # 1920
    0xa4b0, 0xb258, 0x6a50, 0x6d40, 0xada8, 0x2b60, 0x9570, 0x4978, 0x4970, 0x64b0,  # 1930
    0xd4a0, 0xea50, 0x6d48, 0x5ad0, 0x2b60, 0x9370, 0x92e0, 0xc968, 0xc950, 0xd4a0,  # 1940
    0xda50, 0xb550, 0x56a0, 0xaad8, 0x25d0, 0x92d0, 0xc958, 0xa950, 0xb4a8, 0x6ca0,  # 1950
    0xb550, 0x55a8, 0x4da0, 0xa5b0, 0x52b8, 0x52b0, 0xa950, 0xe950, 0x6aa0, 0xad50,  # 1960
    0xab50, 0x4b60, 0xa570, 0xa570, 0x5260, 0xe930, 0xd950, 0x5aa8, 0x56a0, 0x96d0,  # 1970
    0x4ae8, 0x4ad0, 0xa4d0, 0xd268, 0xd250, 0xd528, 0xb540, 0xb6a0, 0x96d0, 0x95b0,  # 1980
    0x49b0, 0xa4b8, 0xa4b0, 0xb258, 0x6a50, 0x6d40, 0xada0, 0xab60, 0x9370, 0x4978,  # 1990
    0x4970, 0x64b0, 0x6a50, 0xea50, 0x6b28, 0x5ac0, 0xab60, 0x9368, 0x92e0, 0xc960,  # 2000
    0xd4a8, 0xd4a0, 0xda50, 0x5aa8, 0x56a0, 0xaad8, 0x25d0, 0x92d0, 0xc958, 0xa950,  # 2010
    0xb4a0, 0xb550, 0xb550, 0x55a8, 0x4ba0, 0xa5b0, 0x52b8, 0x52b0, 0xa930, 0x74a8,  # 2020
    0x6aa0, 0xad50, 0x4da8, 0x4b60, 0x9570, 0xa4e0, 0xd260, 0xe930, 0xd530, 0x5aa0,  # 2030
    0x6b50, 0x96d0, 0x4ae8, 0x4ad0, 0xa4d0, 0xd258, 0xd250, 0xd520, 0xdaa0, 0xb5a0,  # 2040
    0x56d0, 0x4ad8, 0x49b0, 0xa4b8, 0xa4b0, 0xaa50, 0xb528, 0x6d20, 0xada0, 0x55b0,  # 2050
]

_lunar_leap_month = [
    0x00, 0x50, 0x04, 0x00, 0x20,  # 1910
    0x60, 0x05, 0x00, 0x20, 0x70,  # 1920
    0x05, 0x00, 0x40, 0x02, 0x06,  # 1930
    0x00, 0x50, 0x03, 0x07, 0x00,  # 1940
    0x60, 0x04, 0x00, 0x20, 0x70,  # 1950
    0x05, 0x00, 0x30, 0x80, 0x06,  # 1960
    0x00, 0x40, 0x03, 0x07, 0x00,  # 1970
    0x50, 0x04, 0x08, 0x00, 0x60,  # 1980
    0x04, 0x0a, 0x00, 0x60, 0x05,  # 1990
    0x00, 0x30, 0x80, 0x05, 0x00,  # 2000
    0x40, 0x02, 0x07, 0x00, 0x50,  # 2010
    0x04, 0x09, 0x00, 0x60, 0x04,  # 2020
    0x00, 0x20, 0x60, 0x05, 0x00,  # 2030
    0x30, 0xb0, 0x06, 0x00, 0x50,  # 2040
    0x02, 0x07, 0x00, 0x50, 0x03  # 2050
]


def lunar_leap_month(year: int):
    index = (year - 1901) // 2
    pos = (year - 1901 + 1) % 2

    a = _lunar_leap_month[index]
    return a // 2 ** (pos * 4) % 2 ** 4


def lunar_months_day_count(year: int):
    raw = _lunar_months_day_count[year - 1901]
    cnt = 12
    if lunar_leap_month(year):
        cnt = 13
    res = []
    for i in range(1, cnt + 1):
        cur = raw // 2 ** (16 - i) % 2
        if cur == 0:
            res.append(29)
        else:
            res.append(30)

    return res


def is_leap_year(year: int):
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0


def days_of_then_year(dt: datetime.date):
    month_day_count_map = {i + 1: 31 for i in range(12)}
    if is_leap_year(dt.year):
        month_day_count_map[2] = 29
    else:
        month_day_count_map[2] = 28

    for i in (4, 6, 9, 11):
        month_day_count_map[i] = 30

    return sum(v for k, v in month_day_count_map.items() if k < dt.month) + dt.day


def all_days_from_19010101(dt: datetime.date):
    leap_year_count = sum(1 if is_leap_year(y) else 0 for y in range(1901, dt.year))
    return (dt.year - 1901) * 365 + leap_year_count + days_of_then_year(dt)


def lunar_date(all_days: int):
    rest_days = all_days - 49

    lunar_year = 1901
    lunar_year_days = sum(lunar_months_day_count(lunar_year))
    while rest_days > lunar_year_days:
        rest_days -= lunar_year_days
        lunar_year += 1
        lunar_year_days = sum(lunar_months_day_count(lunar_year))

    lunar_month = 1
    lunar_months_day = lunar_months_day_count(lunar_year)
    while rest_days > lunar_months_day[lunar_month - 1]:
        rest_days -= lunar_months_day[lunar_month - 1]
        lunar_month += 1

    lunar_day = rest_days

    this_year_leap_month = lunar_leap_month(lunar_year)

    is_leap_month = False
    if lunar_month > this_year_leap_month > 0:
        lunar_month -= 1
        if lunar_month == this_year_leap_month:
            is_leap_month = True

    return lunar_year, lunar_month, lunar_day, is_leap_month


tiangan = {i: tg for i, tg in enumerate('甲乙丙丁戊己庚辛壬癸')}
dizhi = {i: dz for i, dz in enumerate('子丑寅卯辰巳午未申酉戌亥')}
dizhi_animal = {i: dza for i, dza in enumerate('鼠牛虎兔龙蛇马羊猴鸡狗猪')}

_solar_term_datetime_str_map = {
    '立春': '2022-02-04 04:50:36',
    '雨水': '2022-02-19 00:42:50',
    '惊蛰': '2022-03-05 22:43:34',
    '春分': '2022-03-20 23:33:15',
    '清明': '2022-04-05 03:20:03',
    '谷雨': '2022-04-20 10:24:07',
    '立夏': '2022-05-05 20:25:46',
    '小满': '2022-05-21 09:22:25',
    '芒种': '2022-06-06 00:25:37',
    '夏至': '2022-06-21 17:13:40',
    '小暑': '2022-07-07 10:37:49',
    '大暑': '2022-07-23 04:06:49',
    '立秋': '2022-08-07 20:28:57',
    '处暑': '2022-08-23 11:15:59',
    '白露': '2022-09-07 23:32:07',
    '秋分': '2022-09-23 09:03:31',
    '寒露': '2022-10-08 15:22:16',
    '霜降': '2022-10-23 18:35:31',
    '立冬': '2022-11-07 18:45:18',
    '小雪': '2022-11-22 16:20:18',
    '大雪': '2022-12-07 11:46:04',
    '冬至': '2022-12-22 05:48:01',
    '小寒': '2023-01-05 23:04:39',
    '大寒': '2023-01-20 16:29:20',
}
_solar_term_datetime_map = {k: datetime.datetime.strptime(v, datetime_format) for k, v in _solar_term_datetime_str_map.items()}

_solar_year_seconds = 365.2421990741 * 24 * 3600


def next_solar_term(dt: datetime):
    solar_terms = {k: v for k, v in _solar_term_datetime_map.items()}
    one_solar_year = datetime.timedelta(seconds=_solar_year_seconds)
    for st in solar_terms:
        tm = solar_terms[st]
        while tm < dt:
            tm += one_solar_year

        while tm > dt:
            if dt < tm - one_solar_year:
                tm -= one_solar_year
            else:
                break

        solar_terms[st] = tm

    return min(solar_terms.items(), key=lambda x: x[1])


def last_solar_term(dt: datetime, solar_term: str = None):
    dt += datetime.timedelta(hours=23, minutes=59, seconds=59, microseconds=999999)
    if solar_term:
        solar_terms = {k: v for k, v in _solar_term_datetime_map.items() if k == solar_term}
    else:
        solar_terms = {k: v for k, v in _solar_term_datetime_map.items()}

    one_solar_year = datetime.timedelta(seconds=_solar_year_seconds)
    for st in solar_terms:
        tm = solar_terms[st]
        while tm < dt:
            if tm + one_solar_year > dt:
                break
            else:
                tm += one_solar_year

        while tm > dt:
            tm -= one_solar_year

        solar_terms[st] = tm

    return max(solar_terms.items(), key=lambda x: x[1])


def ganzhi_month(dt: datetime):
    dt += datetime.timedelta(hours=23, minutes=59, seconds=59, microseconds=999999)
    start_dt = _solar_term_datetime_map['立春']
    solar_terms = {k: v for k, v in _solar_term_datetime_map.items() if k in ('立春', '惊蛰', '清明', '立夏', '芒种', '小暑', '立秋', '白露', '寒露', '立冬', '大雪', '小寒')}
    one_solar_year = datetime.timedelta(seconds=_solar_year_seconds)
    res = []
    for st in solar_terms:
        tm = solar_terms[st]
        while tm <= dt:
            if tm > start_dt:
                res.append(tm)
            tm += one_solar_year
    cnt = len(res)
    return f'{tiangan[(cnt + 8) % 10]}{dizhi[(cnt + 2) % 12]}{dizhi_animal[(cnt + 2) % 12]}月'


g_jie = {
    '1-1': '元旦',
    '2-14': '情人节',
    '3-8': '妇女节',
    '3-12': '植树节',
    '3-15': '消费者日',
    '4-1': '愚人节',
    '5-1': '劳动节',
    '5-4': '青年节',
    '6-1': '儿童节',
    '7-1': '建党节',
    '8-1': '建军节',
    '9-10': '教师节',
    '10-1': '国庆节',
    '10-31': '万圣夜',
    '11-11': '光棍节',
    '12-24': '平安夜',
    '12-25': '圣诞节',
}


def is_mothers_day(dt: datetime.date):
    if dt.month != 5:
        return False
    return dt.day == 14 - datetime.date(dt.year, dt.month, 1).weekday()


def is_fathers_day(dt: datetime.date):
    if dt.month != 6:
        return False
    return dt.day == 21 - datetime.date(dt.year, dt.month, 1).weekday()


def is_thanks_giving_day(dt: datetime.date):
    if dt.month != 11:
        return False
    first_weekday = datetime.date(dt.year, dt.month, 1).weekday()
    a = 25
    if first_weekday > 3:
        a += 7
    return dt.day == a - first_weekday


g_jie_func_map = {
    '母亲节': is_mothers_day,
    '父亲节': is_fathers_day,
    '感恩节': is_thanks_giving_day,
}

l_jie = {
    '1-1': '春节',
    '1-15': '元宵',
    '2-2': '龙抬头',
    '5-5': '端午节',
    '6-24': '火把节',
    '7-7': '七夕',
    '7-15': '中元节',
    '8-15': '中秋',
    '9-9': '重阳',
    '12-8': '腊八',
    '12-23': '北方小年',
    '12-24': '南方小年',
}


def is_chuxi(all_days: int):
    next_ldt = lunar_date(all_days + 1)
    if next_ldt[1] == 1 and next_ldt[2] == 1:
        return True

    return False


l_jie_func_map = {
    '除夕': is_chuxi,
}


def ganzhi_year(lunar_year: int):
    tg = tiangan[(lunar_year + 6) % 10]
    dz = dizhi[(lunar_year + 8) % 12]
    dza = dizhi_animal[(lunar_year + 8) % 12]
    return f'{tg}{dz}{dza}年'


def ganzhi_day(all_days: int):
    return f'{tiangan[(all_days + 4) % 10]}{dizhi[(all_days + 2) % 12]}{dizhi_animal[(all_days + 2) % 12]}日'


_weekday = {i: c for i, c in enumerate('一二三四五六日')}


def weekday(dt: datetime.datetime):
    return f'星期{_weekday[dt.weekday()]}'


def g_jie_of(dt: datetime.datetime):
    month_day = f'{dt.month}-{dt.day}'
    res = []
    if month_day in g_jie:
        res.append(g_jie[month_day])
    for k, v in g_jie_func_map.items():
        if v(dt):
            res.append(k)

    return res


def l_jie_of(lunar_month: int, lunar_day: int, all_days: int):
    month_day = f'{lunar_month}-{lunar_day}'
    res = []
    if month_day in l_jie:
        res.append(l_jie[month_day])
    for k, v in l_jie_func_map.items():
        if v(all_days):
            res.append(k)

    return res


def sanfu(dt: datetime.datetime):
    cur_date = last_solar_term(dt, '夏至')[1]
    all_days = all_days_from_19010101(cur_date)
    gengri_count = 0
    for i in range(40):
        gzd = ganzhi_day(all_days)
        if gzd[0] == '庚':
            gengri_count += 1

        if gengri_count == 3:
            break

        cur_date += datetime.timedelta(days=1)
        all_days += 1

    res = [cur_date, cur_date + datetime.timedelta(days=10)]

    cur_date = last_solar_term(dt, '立秋')[1]
    all_days = all_days_from_19010101(cur_date)
    gengri_count = 0
    for i in range(20):
        gzd = ganzhi_day(all_days)
        if gzd[0] == '庚':
            gengri_count += 1

        if gengri_count == 1:
            break

        cur_date += datetime.timedelta(days=1)
        all_days += 1

    res.append(cur_date)

    if dt.strftime(date_format) == res[0].strftime(date_format):
        return '入伏'
    if dt.strftime(date_format) == res[1].strftime(date_format):
        return '中伏'
    if dt.strftime(date_format) == res[2].strftime(date_format):
        return '末伏'


def jiujiu(dt: datetime.datetime):
    cur_date = last_solar_term(dt, '冬至')[1]
    res = [cur_date + datetime.timedelta(days=9 * i) for i in range(9)]
    orders = '一二三四五六七八九'
    for i, d in enumerate(res):
        if dt.strftime(date_format) == d.strftime(date_format):
            return f'{orders[i]}九'


def solar_term(dt: datetime.datetime):
    st, stdt = next_solar_term(dt)
    if stdt.strftime(date_format) == dt.strftime(date_format):
        return st


_lunar_month_str_map = {i + 1: s for i, s in enumerate('正二三四五六七八九十冬腊')}
_lunar_day_str_map = {i + 1: s for i, s in enumerate(['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
                                                      '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
                                                      '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十', ])}


class Calendar:
    def __init__(self, date: datetime.datetime):
        self.date = date
        self.all_days = all_days_from_19010101(self.date)
        self.lunar_year, self.lunar_month, self.lunar_day, self.is_lunar_leap_month = lunar_date(self.all_days)
        self.ganzhi_year = ganzhi_year(self.lunar_year)
        self.ganzhi_month = ganzhi_month(self.date)
        self.ganzhi_day = ganzhi_day(self.all_days)
        self.weekday = weekday(self.date)
        self.g_jie = g_jie_of(self.date)
        self.l_jie = l_jie_of(self.lunar_month, self.lunar_day, self.all_days)
        self.sanfu = sanfu(self.date)
        self.jiujiu = jiujiu(self.date)
        self.solar_term = solar_term(self.date)

    def __str__(self):
        res = [f'{self.date.year}年{self.date.month}月{self.date.day}日 {self.weekday}']
        if self.g_jie:
            res.append('/'.join(self.g_jie))

        res.append(f'农历 {_lunar_month_str_map[self.lunar_month]}月{_lunar_day_str_map[self.lunar_day]} {self.ganzhi_year}-{self.ganzhi_month}-{self.ganzhi_day}')
        if self.solar_term:
            res.append(f'{self.solar_term}')
        if self.sanfu:
            res.append(self.sanfu)
        if self.jiujiu:
            res.append(self.jiujiu)
        if self.l_jie:
            res.append('/'.join(self.l_jie))

        return '\n'.join(res)


if __name__ == '__main__':
    now = datetime.datetime.now()
    today = datetime.datetime(year=now.year, month=now.month, day=now.day)
    print()
    print('今天：')
    print(Calendar(today))
    print('*' * 40)
    print()
    for i in range(1, 32):
        dt = today + datetime.timedelta(days=i)
        c = Calendar(dt)
        if c.g_jie or c.solar_term or c.sanfu or c.jiujiu or c.l_jie:
            print(f'{i}天后：')
            print(c)
            print('*'*40)
            print()
