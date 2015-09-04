# -*- coding: utf-8 -*-


def isiterable(obj, exclude=None):
    '''
    :param exclude: single type or a sequence of types
    '''
    if exclude and isinstance(obj, exclude):
        return False
    try:
        iter(obj)
    except TypeError:
        return False
    return True
