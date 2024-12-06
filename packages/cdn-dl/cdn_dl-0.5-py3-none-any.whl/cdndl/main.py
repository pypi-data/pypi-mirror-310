#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from os import path
import random
from tqdm import tqdm
import urllib3
import ipaddress
from urllib.parse import urlparse
from collections import defaultdict


USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
]


urllib3.disable_warnings()

def is_ip_address(ip_str: str):
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip is not None
    except ValueError:
        return False

def parse_cdn_config(hostname: str, cdn_config: str):
    hostname_ip_map = defaultdict(list)
    file_path = path.join(cdn_config)
    if path.exists(file_path) and path.isfile(file_path):
        # 打开 hosts 文件并逐行读取
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释行
                if not line or line.startswith("#"):
                    continue
                # 拆分行，将第一个字段视为 IP，剩下的字段为主机名
                parts = line.split()
                ip = parts[0]
                hostnames = parts[1:]
                # 将主机名映射到 IP 地址列表
                for hostname in hostnames:
                    hostname_ip_map[hostname].append((ip, 443))
    else:
        ip_port = cdn_config.split(':')
        if len(ip_port) > 2:
            raise SyntaxError('cdn_config仅支持ip或者ip:port 格式!')
        ip = ip_port[0]
        port = int(ip_port[1]) if len(ip_port) == 2 else 443
        if port < 0 or port > 65535:
            raise ValueError('ip 端口应在0-65535!')
        if not is_ip_address(ip):
            raise ValueError('ip 地址不合法!')
        hostname_ip_map[hostname].append((ip, port))
    if not hostname_ip_map:
        raise ValueError('解析cdn 配置失败!')
    return hostname_ip_map


def parse_url(url: str):
    parsed_url = urlparse(url)
    return parsed_url.hostname, parsed_url.path

def download_file(url: str, save_path: str, cdn_config: str, ua: bool, ts: int, timeout: int, retry: int):
    def get_ip_port(hostname: str):
        nonlocal cdn_map
        choices = cdn_map.get(hostname)
        if choices:
            ip, port = random.choice(choices)
        else:
            choices = []
            for _, v in cdn_map.items():
                choices.extend(v)
            ip, port = random.choice(choices)
        return ip, port

    hostname, _ = parse_url(url)
    cdn_map = parse_cdn_config(hostname, cdn_config)
    ip, port = None, None
    headers = {}
    if ua:
        headers.update({'User-Agent': random.choice(USER_AGENTS)})
    while True:
        ip, port = get_ip_port(hostname)
        print('cdn 配置为: {}:{}:{}'.format(hostname, ip, port))
        pool = urllib3.HTTPSConnectionPool(
            ip,
            assert_hostname=hostname,
            server_hostname=hostname,
            port=port,
            cert_reqs='CERT_NONE',
        )
        headers.update({'Host': hostname})
        try:
            response = pool.urlopen('GET', url,
                             redirect=False,
                             headers=headers,
                             assert_same_host=False,
                             timeout=timeout,
                             preload_content=False,
                             retries=urllib3.util.Retry(retry))
            # 检查是否为重定向
            print('请求{} 返回 {}\n'.format(url, response.status))
            if response.status in (301, 302, 303, 307, 308) and 'Location' in response.headers:
                # 获取重定向的 URL
                url = response.headers['Location']
                hostname, _ = parse_url(url)
                # headers = response.headers
                continue
            if response.status == 200:
                total_size = int(response.headers.get('content-length', 0))
                with open(save_path, 'wb') as file, tqdm(
                    desc=save_path,
                    total=total_size,
                    unit='K',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for data in response.stream(ts):
                        file.write(data)
                        bar.update(len(data))
                    response.release_conn()
                    return True
            else:
                raise RuntimeError('请求url: {}返回错误码: {}'.format(url, response.status))
        except Exception as e:
            print('下载文件异常:', e)
            return False

def main():
    parser = argparse.ArgumentParser(description='cdn-dl 下载配置')
    parser.add_argument('-u', '--url', type=str, required=True, help='文件下载url')
    parser.add_argument('-o', '--out', type=str, required=True, help='文件下载路径')
    parser.add_argument('cdn', help='cdn config配置, eg: 1.2.3.4:443 或者hosts 文件')
    parser.add_argument('-ua', '--use_agent', type=bool, default=False, help='是否使用user agent')
    parser.add_argument('-ts', '--trunk_size', type=int, default=8192, help='下载使用的trunk size, 默认8192')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='下载请求超时时间, 默认10s')
    parser.add_argument('-r', '--retry', type=int, default=3, help='下载请求重试次数, 默认3')
    args = parser.parse_args()
    url = args.url
    save_path = path.join(args.out)
    cdn_config = args.cdn
    ua = args.use_agent
    ts = args.trunk_size
    timeout = args.timeout
    retry = args.retry
    res = download_file(url, save_path, cdn_config, ua, ts, timeout, retry)
    msg = '从{} 下载文件到{} {}'.format(url, save_path, '成功' if res else '失败')
    print(msg)

if __name__ == '__main__':
    main()





