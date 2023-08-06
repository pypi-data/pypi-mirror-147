import hashlib
import uuid
from datetime import datetime, date
from typing import List

from dateutil.relativedelta import relativedelta


def md5(s: str):
    m = hashlib.md5()
    m.update(s.encode("utf-8"))
    return m.hexdigest()


def uuid1():
    return uuid.uuid1()


def get_padding_line(text: str, max_len: int = None, padding: str = None) -> str:
    """
    add padding to log text
    "some logs"  ==> "-------- some logs --------"

    :param text: log text
    :param max_len: padding len
    :param padding: padding character, default: -
    :return:
    """
    max_len = max_len or 60
    padding = padding or '-'

    text_len = len(text)
    if (text_len % 2) == 0:
        _size = (max_len - text_len) // 2
        side_str = padding * _size
        return f"{side_str} {text} {side_str}"
    else:
        _size = (max_len - text_len) // 2
        side_str = padding * _size
        return f"{side_str}{padding} {text} {side_str}"


def printl(data: str):
    print(get_padding_line(data))


def change_time(cur_time: datetime = datetime.now(),
                years=0, months=0, days=0, hours=0, minutes=0, seconds=0) -> datetime:
    if isinstance(cur_time, str):
        cur_time: datetime = datetime.strptime(cur_time, '%Y-%m-%d %H:%M:%S')
    return cur_time + relativedelta(
        years=years, months=months, days=days,
        hours=hours, minutes=minutes, seconds=seconds
    )


def change_date(cur_date: date = date.today(), years=0, months=0, days=0) -> date:
    if isinstance(cur_date, str):
        cur_date: date = datetime.strptime(cur_date, '%Y-%m-%d').date()
    return cur_date + relativedelta(
        years=years, months=months, days=days,
    )


def convert_dict_key(data_dict: dict, rule: dict) -> dict:
    if data_dict and rule:
        for k, v in rule.items():
            if k in data_dict:
                data_dict[v] = data_dict.pop(k)
    return data_dict


def convert_list_dict_key(data_list: List[dict], rule: dict) -> list:
    if data_list and rule:
        for data_item in data_list:
            for k, v in rule.items():
                if k in data_item:
                    data_item[v] = data_item.pop(k)
    return data_list
