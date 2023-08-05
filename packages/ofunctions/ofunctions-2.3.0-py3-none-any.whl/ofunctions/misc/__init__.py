#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of ofunctions package

"""
ofunctions is a general library for basic repetitive tasks that should be no brainers :)

Versioning semantics:
    Major version: backward compatibility breaking changes
    Minor version: New functionality
    Patch version: Backwards compatible bug fixes

"""

__intname__ = "ofunctions.misc"
__author__ = "Orsiris de Jong"
__copyright__ = "Copyright (C) 2014-2022 Orsiris de Jong"
__description__ = "Collection of various functions"
__licence__ = "BSD 3 Clause"
__version__ = "1.2.0"
__build__ = "2021060301"
__compat__ = "python2.7+"


# python 2.7 compat fixes
try:
    from typing import Optional, List, Any
except ImportError:
    pass


# Restrict number n between minimum and maximum
restrict_numbers = lambda n, n_min, n_max: max(min(n_max, n), n_min)


def rot13(string):
    # type: (str) -> Optional[str]
    """
    Rot13 for only A-Z and a-z characters
    """
    try:
        return "".join(
            [
                chr(ord(n) + (13 if "Z" < n < "n" or n < "N" else -13))
                if ("a" <= n <= "z" or "A" <= n <= "Z")
                else n
                for n in string
            ]
        )
    except TypeError:
        return None


def bytes_to_string(bytes_to_convert, strip_null=False):
    # type: (List[int], bool) -> Optional[str]
    """
    Litteral bytes to string
    :param bytes_to_convert: list of bytes in integer format
    :param strip_null: Remove trailing and ending null bytes
    :return: resulting string
    """
    try:
        value = "".join(chr(i) for i in bytes_to_convert)
        if strip_null:
            return value.strip("\x00")
        return value
    # AttributeError when None object has no strip attribute
    except (ValueError, TypeError, AttributeError):
        return None


def time_is_between(current_time, time_range):
    # type: (str, tuple) -> bool
    """
    https://stackoverflow.com/a/45265202/2635443
    print(is_between("11:00", ("09:00", "16:00")))  # True
    print(is_between("17:00", ("09:00", "16:00")))  # False
    print(is_between("01:15", ("21:30", "04:30")))  # True
    """

    if time_range[1] < time_range[0]:
        return current_time >= time_range[0] or current_time <= time_range[1]
    return time_range[0] <= current_time <= time_range[1]


def reverse_dict(dictionary):
    # type: (dict) -> dict
    """
    Return a reversed dictionary ie {value: key}
    """
    return {value: key for key, value in dictionary.items()}


def get_key_from_value(haystack, needle):
    # type: (dict, str) -> str
    """
    Returns a dict key by it's value, ie get_key_from_value({key: value}, value) returns key
    """
    return next((k for k, v in haystack.items() if v == needle), None)


def is_nan(var):
    # type: (Any) -> bool
    """
    Simple check if a variable is a numpy NaN
    based on the simple check where (nan is nan) gives True but (nan == nan) gives False
    """
    return not var == var
