#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from ..util import post_urlencoded_data as post

API = 'https://dnsapi.cn/Record.List'
PARAMS = {
    'login_token': '',
    'domain': 'logi.ml',
    'sub_domain': 'n1',
    'format': 'json',
    'lang': 'en',
    'error_on_empty': 'yes'
}
GATE_WAY = ''


def gen_error(key, content={}):
    return {
        'default': {
            'code': -1,
            'error': 'lack of params.',
            'example': GATE_WAY + '?domain=baidu.com&subDomain=www'
        },
        'success': {
            'code': 0,
            'msg': 'success',
            **content
        },
        'none': {
            'code': 3,
            'error': 'no record.',
        },
        'server': {
            'code': 2,
            'error': 'dnspod server error.',
        }
    }[key]


def query(gateway, queryString):
    global GATE_WAY
    GATE_WAY = gateway
    if 'domain' in queryString and 'subDomain' in queryString:
        PARAMS['domain'] = queryString['domain']
        PARAMS['sub_domain'] = queryString['subDomain']
    else:
        return gen_error('default')

    try:
        record = json.loads(post(API, PARAMS).text)
    except Exception:
        return gen_error('server')

    try:
        return gen_error('success', {
            'address': PARAMS['sub_domain'] + '.' + PARAMS['domain'],
            'ip': record['records'][0]['value'],
            'updated_on': record['records'][0]['updated_on']
        })
    except Exception:
        return gen_error('none')
