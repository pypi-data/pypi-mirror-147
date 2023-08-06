#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The tools.
"""
from collections.abc import Iterable
import os
import json
import itertools
import tkinter as tk


def Reprlist_inster_use(a, i, lo):
    if len(i) > 1 and len(set(i)) == 1:
        j = i[0].ljust(lo)
        if len(j) > lo:
            i.append(a)
        else:
            i.append(j)
    else:
        i.append(a)


def iterable(obj):
    return isinstance(obj, Iterable)


def shape(obj):
    if isinstance(obj, str):
        return (len(obj),),
    obj = list(obj)
    if len(obj) == 0:
        return 0,
    r = ()
    try:
        n = [len(i) for i in obj]
    except TypeError:
        if all(not iterable(i) or isinstance(i, str) for i in obj):
            return (tuple(len(str(i)) for i in obj),)
    else:
        ts = {type(i) for i in obj}
        if ts == {str}:
            return (tuple(n),)
        if len(ts) == 1:
            if len(set(n)) == 1:
                r += (len(n),)
                return r + shape(obj[0])
            for i in obj:
                for j in i:
                    if not \
                            not iterable(j) or isinstance(j, str):
                        l = {sum(len(str(j)) for j in i) for i in obj}
                        if len(l) == 1:
                            return r + (len(n),) + (tuple(l),)
                        else:
                            raise ValueError("Irregular iterable got.")
        else:
            raise ValueError("Irregular iterable got.")


def reshape(val, nd):
    if all(iterable(i) for i in val):
        if all(isinstance(i, str) for i in val):
            s = p = 0
            r = []
            val = ''.join(val)
            for i in nd:
                p = p + i
                r.append(val[s:p])
                s = p
            return r
        else:
            r = []
            for i in val:
                r.append(reshape(i, nd))
            return r
    else:
        return reshape([str(i) for i in val], nd)


def get_global_config():
    with open(os.path.join(os.path.dirname(__file__), 'config_global.json'), encoding="utf-8") as fp:
        return json.load(fp)


def _check_rule_value(old):
    if any(not ((isinstance(i, int) and i > 3) or i is None)
           for i in (old['maxstring'],
                     old['maxline'])):
        raise ValueError("Key 'maxstring','maxline' need be int and > 3.")
    if not isinstance(old['startswith'], str):
        raise TypeError("key 'startswith' need str, got",
                        type(old['startswith']))


def check_rule_value(dic):
    _check_rule_value(dic['r'])
    _check_rule_value(dic['s'])
    _check_rule_value(dic['f'])
    if not isinstance(dic['f']['linebreaks'], str):
        raise TypeError('The line breaks need be str. got ',
                        type(dic['f']['linebreaks']))


def _set_maxstring(n):
    if n is None:
        def gen(iterable):
            'A func complexed by `complex_rule`.'
            return iterable
    else:
        n1 = (n + 1) // 2
        n2 = n1 - n

        def gen(iterable):
            'A func complexed by `complex_rule`.'
            if len(iterable) > n:
                return '...'.join([iterable[:n1], iterable[n2:]])
            else:
                return iterable
    return gen


def _set_maxline(n):
    if n is None:
        def gen(iterable):
            'A func complexed by `complex_rule`.'
            return enumerate(iterable)
    else:
        n1 = (n + 1) // 2
        n2 = n1 - n

        def gen(iterable):
            'A func complexed by `complex_rule`.'
            l = len(iterable)
            if l < n:
                yield from enumerate(iterable)
            else:
                yield from enumerate(iterable[:n1])
                yield from (('.', '',),) * 3
                yield from enumerate(iterable[n2:], l - n1)
    return gen


def comp_rule(dic):
    rst = []
    for k in 'rs':
        rst.append(_set_maxstring(dic[k]['maxstring']))
        rst.append(_set_maxline(dic[k]['maxline']))
    else:
        return rst
