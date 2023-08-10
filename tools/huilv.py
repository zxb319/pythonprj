import json

import requests

session = requests.Session()


def dict_raw_headers(headers_str: str):
    a = headers_str.split('\n')
    a = [x.split(':') for x in a]
    a = [x for x in a if len(x) == 2]
    return {x[0].strip(): x[1].strip() for x in a}


def get_huilv_per_cny(from_money: str):
    headers = """
        Accept: */*
        Accept-Encoding: gzip, deflate, br
        Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6
        Connection: keep-alive
        Cookie: BIDUPSID=FD70D57EE1D64F8599BBDF9C8FCECBD9; PSTM=1603529350; BDUSS=WRZa0xUdzBMbEw3WjNYLWdNMUdNVG10S09TZmhQWH5iRWREME9HUElwdVB4cnhmSVFBQUFBJCQAAAAAAAAAAAEAAACb9qIn1cXQwrKoMzE5NgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI85lV-POZVfd; BDUSS_BFESS=WRZa0xUdzBMbEw3WjNYLWdNMUdNVG10S09TZmhQWH5iRWREME9HUElwdVB4cnhmSVFBQUFBJCQAAAAAAAAAAAEAAACb9qIn1cXQwrKoMzE5NgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI85lV-POZVfd; MCITY=-%3A; BAIDUID=735ED07FC8FA95C5AECF3DB9A50C2BCD:SL=0:NR=10:FG=1; H_PS_PSSID=38515_36550_38687_38881_38793_38817_38839_38636_38847_26350_38570_22159; BAIDUID_BFESS=735ED07FC8FA95C5AECF3DB9A50C2BCD:SL=0:NR=10:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598
        Host: sp0.baidu.com
        Referer: https://www.baidu.com/s?wd=%E6%B1%87%E7%8E%87%E6%8D%A2%E7%AE%97&rsv_spt=1&rsv_iqid=0xcc20062c00052cc3&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=ib&rsv_n=2&rsv_sug3=1
        Sec-Fetch-Dest: script
        Sec-Fetch-Mode: no-cors
        Sec-Fetch-Site: same-site
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
        sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"
        sec-ch-ua-mobile: ?0
        sec-ch-ua-platform: "Windows"
    """
    url = rf'https://sp0.baidu.com/5LMDcjW6BwF3otqbppnN2DJv/finance.pae.baidu.com/vapi/async?from_money={from_money}&to_money=%E4%BA%BA%E6%B0%91%E5%B8%81&from_money_num=1&srcid=5293&sid=38515_36550_38687_38881_38793_38817_38839_38636_38847_26350_38570_22159&cb=jsonp_1687620006779_2476'
    headers = dict_raw_headers(headers)

    resp = session.get(url, headers=headers)

    res = json.loads(resp.text[len('jsonp_1687620006779_2476('):-1])
    return float(res['Result'][0]['DisplayData']['resultData']['tplData']['money2_num'])


MONEYS = [
    '日元', '英镑', '港元', '加元', '美元', '欧元', '韩元', '澳元', '缅甸元', '澳门元', '俄罗斯卢布', '泰铢',
]

if __name__ == '__main__':
    res = [(m, get_huilv_per_cny(m)) for m in MONEYS]
    res = sorted(res, key=lambda x: x[1], reverse=True)
    for m, n in res:
        print(m, n, f'1人民币\t==\t{round(1 / n, 2)}{m}',sep='\t')
