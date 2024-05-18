import json
import requests

session = requests.Session()


def dict_raw_headers(headers_str: str):
    a = headers_str.split('\n')
    a = [x.split(':') for x in a]
    a = [x for x in a if len(x) >= 2]
    return {x[0].strip(): ':'.join(x[1:]).strip() for x in a}


def get_huilvs():
    headers = """
        Accept: application/vnd.finance-web.v1+json
        Accept-Encoding: gzip, deflate, br
        Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
        Acs-Token: 1711638121992_1711714212688_FqDbceACq26Z+C6wBwhlWldq2Yh6vgwqi7ynYYrVd3CP5VzzxthjfRRRNO6EHNONO7BxWZFAtWsQeRkQxLDmFiJyTWrUdGMJQesua5AM8QjCpTLp2HhXR7mi3W+hAAY3ksBgq7tBBWMCPOsU2A041lJxrrnO98NLqtTFiaIv8MRxQebyyxR6C2/jvImakpHmUAfsNdS3QXeFKWLaMoy97kkGgWGmtRJbyPgjbUl5StqiS734T4jI3oYWSF+FernPPRhyBDYhq6W8Vjexr3k69cYHmVE+fm8tGhQNsE7wnNnc0mVsJKdeYKJZvCdfJP8hjRykarqQSpUxU8XCDq+Z5mm2ZMu1ZY9gDBsrjkLoiCqRraYZKpmbACXEKAz3mCbG+zRt7JtBzM2+Z4pwE/vAWwtlk6f/C8ys5+b3aH0IFvYn/Iql3dQMO9JBQvi4UGHAZgAv9tGymatMRqsnWbfWGg==
        Connection: keep-alive
        Cookie: BIDUPSID=3911ED513E5183211F5CCCC4EDB179C3; PSTM=1603528173; BDUSS=hBNFdUUTJ1WnBUTHpxSX5hSHlMMlNoNUdmT2ozSVQ0Smk4aFhXeUlOY0xjSHRpSVFBQUFBJCQAAAAAAAAAAAEAAACb9qIn1cXQwrKoMzE5NgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAvjU2IL41NiWW; BDUSS_BFESS=hBNFdUUTJ1WnBUTHpxSX5hSHlMMlNoNUdmT2ozSVQ0Smk4aFhXeUlOY0xjSHRpSVFBQUFBJCQAAAAAAAAAAAEAAACb9qIn1cXQwrKoMzE5NgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAvjU2IL41NiWW; BAIDUID=98FE10D3647D999B8C806FFE12CB7BAD:SL=0:NR=10:FG=1; MCITY=-289%3A; H_WISE_SIDS=40080_40304_40376_40416_40446_40464_40459_40457_40317_40510_40398_60044_60033_60046; BAIDUID_BFESS=98FE10D3647D999B8C806FFE12CB7BAD:SL=0:NR=10:FG=1; ZFY=ELhmriCmnOkCrTXldNHZmPxnxTHYnX1kSm8pBmhgyA8:C; H_WISE_SIDS_BFESS=40080_40304_40376_40416_40446_40464_40459_40457_40317_40510_40398_60044_60033_60046; BAIDU_WISE_UID=wapp_1711553705956_306; RT="z=1&dm=baidu.com&si=fa61fe4a-0a43-4dd3-af86-8f61c39051ef&ss=lu9yvu36&sl=6&tt=2dd&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=15m9c&ul=15n5t&hd=15n6p"; H_PS_PSSID=40080_40304_40376_40416_40446_40464_40459_40457_40510_40398_60044_60033_60046; BA_HECTOR=25ala580008g2g840h048la4sqqbeo1j0dbs81s; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=5; delPer=0; ab_sr=1.0.1_NjkwY2U2ZGVhZDYwMDVmOTRhNTM1MDMzOThhY2ZhYmJhNGU2N2ExZDJjNjZkYTJlNzI4OWE5M2YwYjNlZDE5ZmI4MGExYTljZTcxYmMzNjU4Mzc2M2E3OGU3NTVkOGM4NWExMjg5NTg4ZmY1OTQ2YjE3YWY0ODUyOTRjMmYyMTAxOTAyNWJjYjlmY2E2YmE4ZDRkZWFmZmI5M2VmNmIxMmZlNzAxNTMwYjAxNmRhNzJkMjRmNDg2YjkxZmYwZGFhYTM0ZjhmYzY5YzE5OTAxYTZlMjA2ZDdmZmFlZTExOGI=
        Host: finance.pae.baidu.com
        Origin: https://gushitong.baidu.com
        Referer: https://gushitong.baidu.com/
        Sec-Fetch-Dest: empty
        Sec-Fetch-Mode: cors
        Sec-Fetch-Site: same-site
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0
        sec-ch-ua: "Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"
        sec-ch-ua-mobile: ?0
        sec-ch-ua-platform: "Windows"
    """

    headers = dict_raw_headers(headers)
    page_no = 0
    res = []
    while True:
        url = rf'https://finance.pae.baidu.com/api/getforeignrank?pn={page_no}&rn=100&type=rmb&finClientType=pc'
        resp = session.get(url, headers=headers)
        cur = json.loads(resp.content)
        cur = cur['Result']
        res.extend(cur)
        if len(cur) < 100:
            break
        page_no += 100

    ret = []
    for r in res:
        cur = {'name': r['name'][3:]}
        for x in r['list']:
            if x['text'] == '最新价':
                v = float(x['value'])
                cur['value'] = 1 / v if v else None
                if v and v > 1:
                    cur['1元人民币能兑换'] = v

        ret.append(cur)
    return sorted((r for r in ret if r['value'] is not None), key=lambda x: x['value'], reverse=True)


if __name__ == '__main__':
    rrr = get_huilvs()
    print(*enumerate(rrr), sep='\n')
    # lI1o0O
