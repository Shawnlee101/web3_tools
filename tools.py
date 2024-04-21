import requests
import json
from datetime import datetime
import secrets
import string
from eth_account import Account
from eth_account.messages import encode_defunct
import time


def get_proxy(proxy: str) -> dict:
    """
    转化格式为发送请求【proxies】参数可接受的类型
    :param proxy: 格式："185.245.26.85:6602:rtshntgw:xn082v1f9k8d"或者"rtshntgw:xn082v1f9k8d@185.245.26.85:6602"
    :return: {
            'http': 'http://rtshntgw:xn082v1f9k8d@185.245.26.85:6602',
            'https': 'http://rtshntgw:xn082v1f9k8d@185.245.26.85:6602'
        }
    """
    if proxy.find('@') == 1:
        proxy = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        return proxy
    else:
        proxy_list = proxy.split(':')
        proxy = {
            'http': f'http://{proxy_list[2]}:{proxy_list[3]}@{proxy_list[0]}:{proxy_list[1]}',
            'https': f'http://{proxy_list[2]}:{proxy_list[3]}@{proxy_list[0]}:{proxy_list[1]}'
        }
        return proxy


def get_ip(proxy=None) -> str:
    """
    查询ip地址
    :param proxy: 要查询的代理
    :return: 代理的ip地址
    """
    ip_response = requests.get("https://api64.ipify.org?format=json",
                               proxies=proxy)
    ip_address_dict = json.loads(ip_response.text)
    ip_address = ip_address_dict['ip']
    return ip_address


def generate_js_time_format(now=None) -> str:
    """
    处理登录时message弹窗出现时间戳
    :param now: None
    :return: 时间戳
    """
    if now is None:
        now = datetime.now()
    a = now.strftime("%Y-%m-%dT%H:%M:%S")
    b = now.strftime("%f")[:3]
    now_format_string = f"{a}.{b}Z"
    # print(now_format_string)
    return now_format_string


def generate_nonce(nonce_type: str, nonce_length: int) -> str:
    """
    获取登陆时的随机数
    :param nonce_type: 随机数类型 'mix', 'digit', or 'letters'
    :param nonce_length: 随机数长度
    :return: 随机数字符串
    """
    if nonce_type == "mix":
        nonce_material = string.ascii_letters + string.digits
        return "".join(secrets.choice(nonce_material) for _ in range(nonce_length))
    elif nonce_type == "digit":
        nonce_material = string.digits
        return "".join(secrets.choice(nonce_material) for _ in range(nonce_length))
    elif nonce_type == "letters":
        nonce_material = string.ascii_letters
        return "".join(secrets.choice(nonce_material) for _ in range(nonce_length))
    else:
        raise ValueError("Invalid nonce_type. Expected one of 'mix', 'digit', or 'letters'.")
