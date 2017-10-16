#!/usr/bin/python3
# _*_ coding:utf-8 _*_

"""
命令行查询火车票余票

Usage:
    python ticket.py [-dgktz] <from> <to> <date>

Options:
    -h --help       显示帮助
    -d              动车
    -g              高铁
    -k              快速
    -t              特快
    -z              直达

Example:
    python tickets.py 上海 苏州 2017-10-20
    python tickets.py -dg 上海 苏州 2017-10-20
    python tickets.py -g 上海 苏州 2017-10-20

"""

__author__ = 'Svend'

import stations
import requests
from docopt import docopt
from prettytable import PrettyTable
from colorama import Fore
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

version = 'Tickets 1.0'


class Util:
    @staticmethod
    def colored(color, target):
        return ''.join([getattr(Fore, color.upper()), target, Fore.RESET])


class TrainCollection:
    headers = '车次|车站|时间|历时|商务(特等)座|一等座|二等座|高级软卧|软卧|动卧|硬卧|软座|硬座|无座|其他|二代身份证直接进出站'.split('|')

    def __init__(self, raw_trains, options):
        self.raw_trains = raw_trains
        self.options = options

    def get_from_to_station_names(self, data_list):
        from_station_code = data_list[6]
        to_station_code = data_list[7]
        return '\n'.join([
            Util.colored('green', stations.get_name(from_station_code)),
            Util.colored('red', stations.get_name(to_station_code))
        ])

    def get_start_arrive_time(self, data_list):
        start_time = data_list[8]
        arrive_time = data_list[9]
        return '\n'.join([
            Util.colored('green', start_time),
            Util.colored('red', arrive_time)
        ])

    def parse_train_data(self, data_list):
        train_code = data_list[3]
        from_to_station_name = self.get_from_to_station_names(data_list)
        start_arrive_time = self.get_start_arrive_time(data_list)
        time_duration = data_list[10]
        business_class_seat = data_list[32] or data_list[25] or '--'
        first_class_seat = data_list[31] or '--'
        second_class_seat = data_list[30] or '--'
        senior_soft_sleep = data_list[21] or '--'
        soft_sleep = data_list[23] or '--'
        move_seat = data_list[33] or '--'  # 动卧
        hard_sleep = data_list[28] or '--'
        soft_seat = data_list[24] or '--'
        hard_seat = data_list[29] or '--'
        no_seat = data_list[26] or '--'
        other = data_list[22] or '--'

        is_support_card = int(data_list[18] or 0)
        is_support_card = Util.colored('green', u'支持') if is_support_card else Util.colored('red', u'不支持')

        return [train_code, from_to_station_name, start_arrive_time, time_duration,
                business_class_seat, first_class_seat, second_class_seat, senior_soft_sleep,
                soft_sleep, move_seat, hard_sleep, soft_seat, hard_seat, no_seat, other, is_support_card]

    def filter_train(self, data_list):
        train_code = data_list[3]
        initial = train_code[0].lower()
        return not self.options or initial in self.options

    @property
    def trains(self):
        for train in self.raw_trains:
            data_list = train.split('|')
            if self.filter_train(data_list):
                train_data = self.parse_train_data(data_list)
                yield train_data

    def pretty_print(self):
        pt = PrettyTable(self.headers)
        for train in self.trains:
            pt.add_row(train)
        print(pt)


class Cli:
    via_url = ('https://kyfw.12306.cn/otn/leftTicket/query?'
               'leftTicketDTO.train_date={date}&'
               'leftTicketDTO.from_station={from_station}&'
               'leftTicketDTO.to_station={to_station}&'
               'purpose_codes=ADULT')

    def __init__(self):
        self.arguments = docopt(__doc__, version=version)
        self.from_station = stations.get_telecode(self.arguments['<from>'])
        self.to_station = stations.get_telecode(self.arguments['<to>'])
        self.date = self.arguments['<date>']
        self.validate_arguments()
        self.options = ''.join([key for key, value in self.arguments.items() if value is True])

    def validate_arguments(self):
        if self.from_station is None or self.to_station is None:
            print(Util.colored('red', u'请输入有效的车站名称！'))
            exit(0)

        try:
            if datetime.strptime(self.date, '%Y-%m-%d') < datetime.now():
                print(Util.colored('red', u'请输入有效日期！'))
                exit(0)
        except ValueError:
            print(Util.colored('red', u'请输入正确的日期格式！'))
            exit(0)

    def run(self):
        url = self.via_url.format(date=self.date, from_station=self.from_station, to_station=self.to_station)
        response = requests.get(url, verify=False)
        result = response.json()
        if 'data' not in result:
            msg = result.get('messages', None)
            if msg is not None:
                print(Util.colored('red', ','.join(msg)))
            else:
                print(Util.colored('red', u'获取车次信息失败！ 请联系管理员 svend.jin@qq.com'))
            exit(0)
        raw_trains = result['data']['result']
        tc = TrainCollection(raw_trains, self.options)
        tc.pretty_print()


if __name__ == '__main__':
    Cli().run()
