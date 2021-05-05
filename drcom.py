#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 19:50:29 2018

@author: wuxiaobai24
"""

import requests
import time
import os
import sys
import argparse
import logging


username=""
passwd = ""
url = 'http://172.30.255.2/a30.htm'

parser = argparse.ArgumentParser(description='a script for login dr.com in SZU')
parser.add_argument('--daemon', '-d',
                    dest='daemon',
                    action='store_true', 
                    help='whether become daemon')
parser.add_argument('--username', '-u', type=str, required=True,
                    dest='username',
                    help = 'username')
parser.add_argument('--passwd', '-p', type=str,
                    dest='password', required=True,
                    help = 'password')

parser.add_argument('--gap', '-g', type=int,
                    dest='gap', default=5 * 60,
                    help = 'check gap(second)')

parser.add_argument('--drcom', help='use drcom.szu.edu.cn as login url', action='store_true')
parser.add_argument('--url', help='login url', type=str, default = None)

logging.basicConfig(filename='drcom.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def tryLogin(gap):
    while True:
        if isLogin():
            time.sleep(gap)
        else:
            login()


def daemon():
    '''become daemon'''
    logging.info('become daemon')
    logging.info('PID is %d' % os.getpid())
    file_path = os.path.abspath('.') + '/kill_daemon.sh'
    logging.info('kill shell in {}'.format(file_path))
    
    pid = os.fork()
    if pid:
        # father process exit
        sys.exit(0)
    os.chdir('/')
    os.umask(0)
    os.setsid()
    sys.stderr.flush()
    sys.stdout.flush()

    with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
        os.dup2(read_null.fileno(), sys.stdin.fileno())
        os.dup2(write_null.fileno(), sys.stderr.fileno())
        os.dup2(write_null.fileno(), sys.stdout.fileno())

    # save the kill shell

    s = "#!/bin/bash\nkill %d\nrm %s" % (os.getpid(), file_path)
    with open(file_path, 'w') as f:
        f.write(s)
    
    os.system('chmod +x %s' % file_path)

def login():
    logging.info('login')
    headers = {}
    headers['Accept'] = 'ext/html,application/xhtml+xml,application/xml' \
    ';q=0.9,*/*;q=0.8r'
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) ' \
    'Gecko/20100101 Firefox/58.0'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    # headers['Content-Length'] = '51'

    data = {'0MKKey': '登　录'.encode('gb2312'),
            'DDDDD': username,
            'upass': passwd}
    r = requests.post(url, data=data, headers=headers)
    r.encoding = 'gb2312'
    print(r.text)
    if '您已经成功登录。' in r.text:
        logging.info('Login Success')
        return True
    else:
        logging.info('Login Fail')
        return False


def isLogin():
    try:
        r = requests.get('http://www.baidu.com/', timeout=10, allow_redirects=False)
        if r.status_code != requests.status_codes.codes.ok:
            logging.info('isLogin return False, status_code is {}'.format(r.status_code))
            return False
        else:
            logging.info('isLogin return True')
            return True
    except Exception as e:
        logging.info('isLogin Exception: {}'.format(e))
        return False


if __name__ == '__main__':
    args = parser.parse_args()
    if args.daemon:
        daemon()
    username = args.username
    passwd = args.password
    gap = args.gap

    if args.drcom:
        url = "https://drcom.szu.edu.cn"
    if args.url:
        url = args.url
    logging.info('Url is {}'.format(url))

    logging.info('Gap is {}'.format(gap))
    if gap <= 0:
        login()
    else:
        tryLogin(gap)
    logging.info('Exit')
