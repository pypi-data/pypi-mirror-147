# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, C0301
from dataskema import lang


def trim(string: str):
    if string is None:
        return ''
    if not isinstance(string, str):
        string = str(string)
    return string.strip(' \t\r\n')


def is_empty(value: str) -> bool:
    return value is None or trim(str(value)) == ''


def log_value(value):
    value = str(value)
    if len(value) > 10:
        value = value[0:10] + '...'
    return value


def typeof(value) -> str or None:
    stype = str(type(value))
    idx1 = stype.find("'")
    idx2 = stype.rfind("'")
    if idx2 <= idx1:
        raise RuntimeError(lang.get_message(ERROR_TYPE_NOT_FOUND, {'stype': stype}))
    stype = stype[idx1 + 1:idx2]
    if stype == 'NoneType':
        return None
    return stype
