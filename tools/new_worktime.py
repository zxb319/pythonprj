import base64
import json

import Crypto.Random
import requests

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def generate_aes_key(size=16):
    return Crypto.Random.get_random_bytes(size)


def aes_encrypt(msg, key):
    aes = AES.new(key, AES.MODE_CBC)
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    padded_msg = pad(msg, AES.block_size)
    return aes.encrypt(padded_msg)

def aes_decrypt(msg, key):
    aes = AES.new(key, AES.MODE_CBC)
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    padded_msg = pad(msg, AES.block_size)
    return aes.decrypt(padded_msg)

def rsa_encrypt(msg, pub_key):
    pub_key = rf'''-----BEGIN RSA PUBLIC KEY-----
{pub_key}
-----END RSA PUBLIC KEY-----'''
    pub_key = RSA.import_key(pub_key)
    rsa = PKCS1_v1_5.new(pub_key)
    encrypted = rsa.encrypt(msg.encode('utf-8'))
    encrypted = base64.b64encode(encrypted).decode('utf-8')
    return encrypted


def headers_str_to_dict(headers_str: str):
    headers = headers_str.split('\n')
    headers = [h.split(':') for h in headers]
    headers = [h for h in headers if len(h) >= 2]
    return {
        h[0].strip(): ':'.join(h[1:]).strip() for h in headers
    }


user_id = '335524'
user_pwd = 'gbbscsyrrd319!'


class Agent:
    def __init__(self, user_id=user_id, user_pwd=user_pwd):
        self.user_id = user_id
        self.user_pwd = user_pwd
        self.session = requests.session()

    def getPublicKey(self):
        headers = rf'''
                Accept: */*
                Accept-Encoding: gzip, deflate, br
                Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
                Connection: keep-alive
                Host: ics.chinasoftinc.com
                Referer: https://ics.chinasoftinc.com/SignOnServlet
                Sec-Fetch-Dest: empty
                Sec-Fetch-Mode: cors
                Sec-Fetch-Site: same-origin
                User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0
                X-Requested-With: XMLHttpRequest
                sec-ch-ua: "Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"
                sec-ch-ua-mobile: ?0
                sec-ch-ua-platform: "Windows"
        '''
        url = rf'https://ics.chinasoftinc.com/r1portal/getPublicKey'
        headers = headers_str_to_dict(headers)
        resp = self.session.get(url, headers=headers, verify=False, allow_redirects=False)
        try:
            res = json.loads(resp.text)
        except:
            res = {}

        if not isinstance(res, dict) or res.get('code') != 200:
            raise Exception(resp.text)

        self.rsaPublicKey = res['data']['rsaPublicKey']
        self.traceNo = res['traceNo']


if __name__ == '__main__':
    a='jddEEO08YSwSRAfUtnTrKA=='
    print(base64.b64decode(a))