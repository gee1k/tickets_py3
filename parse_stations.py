#!/usr/bin/python3
# _*_ coding:utf-8 _*_

__author__ = 'Svend'

import re
import requests
import pickle

stations_names_url ='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version={version}'
stations_names_version ='1.9027'


def parse():
    url = stations_names_url.format(version=stations_names_version)
    response = requests.get(url, verify=False)
    pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
    result = dict(re.findall(pattern, response.text))
    stastions = {
        'names': list(result.keys()),
        'telecodes': list(result.values())
    }

    with open('stations.pkl', 'wb') as f:
        pickle.dump(stastions, f)


if __name__ == '__main__':
    parse()