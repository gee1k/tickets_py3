#!/usr/bin/python3
# _*_ coding:utf-8 _*_

__author__ = 'Svend'

import pickle

_stations_names = []
_stations_codes = []


def _initial_stations():
    global _stations_names
    global _stations_codes
    with open('stations.pkl', 'rb') as f:
        result = pickle.load(f)
        _stations_names = result['names']
        _stations_codes = result['telecodes']


def get_name(code):
    return _stations_names[_stations_codes.index(code)]


def get_telecode(name):
    return _stations_codes[_stations_names.index(name)]


_initial_stations()