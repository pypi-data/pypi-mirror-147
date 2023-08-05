"""
Class functions.

Usage:
 ./utils/tools/_class_functions.py

Author:
 Peter Rigali - 2022-03-30
"""
from typing import Union


# Model_data
def _names(n: str, n_lst: Union[list, tuple]) -> bool:
    name_dic = {name: True for name in n_lst}
    if n not in name_dic:
        return True
    else:
        raise AttributeError("{} already included in names list".format(n))


def _len(l1: int, l2: int) -> bool:
    if l1 == l2:
        return True
    else:
        raise AttributeError("(len1: {} ,len2: {} ) Lengths are not the same.".format(l1, l2))


def _get_fit_pred(data, fp: str, ttv: str):
    if fp == 'fit':
        return {'train': (data.x_train, data.y_train), 'test': (data.x_test, data.y_test),
                'valid': (data.x_valid, data.y_valid)}[ttv]
    elif fp == 'pred':
        return {'train': data.x_train, 'test': data.x_test, 'valid': data.x_valid}[ttv]
    elif fp == 'score':
        return {'train': data.y_train, 'test': data.y_test, 'valid': data.y_valid}[ttv]
