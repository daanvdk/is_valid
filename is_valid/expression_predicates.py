import re

from .condition_predicates import is_all, is_any
from .type_predicates import is_str


def is_eq(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, detailed=False):
        if not detailed:
            return data == value
        return (
            False, 'data is not equal to {}'.format(rep)
        ) if not data == value else (True, None)
    return is_valid


def is_neq(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, detailed=False):
        if not detailed:
            return data != value
        return (
            False, 'data is not not equal to {}'.format(rep)
        ) if not data != value else (True, None)
    return is_valid


def is_gt(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, detailed=False):
        if not detailed:
            return data > value
        return (
            False, 'data is not greater than {}'.format(rep)
        ) if not data > value else (True, None)
    return is_valid


def is_geq(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, detailed=False):
        if not detailed:
            return data >= value
        return (
            False, 'data is not greater than or equal to {}'.format(rep)
        ) if not data >= value else (True, None)
    return is_valid


def is_lt(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, detailed=False):
        if not detailed:
            return data < value
        return (
            False, 'data is not lower than {}'.format(rep)
        ) if not data < value else (True, None)
    return is_valid


def is_leq(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, detailed=False):
        if not detailed:
            return data <= value
        return (
            False, 'data is not lower than or equal to {}'.format(rep)
        ) if not data <= value else (True, None)
    return is_valid


def is_in_range(start, stop, start_in=True, stop_in=False):
    return is_all(
        (is_geq if start_in else is_gt)(start),
        (is_leq if stop_in else is_lt)(stop)
    )


def is_not_in_range(start, stop, start_in=True, stop_in=False):
    return is_any(
        (is_lt if start_in else is_leq)(start),
        (is_gt if stop_in else is_geq)(stop)
    )


def is_in(collection):
    def is_valid(data, detailed=False):
        if not detailed:
            return data in collection
        return (
            False, 'data is not in collection'
        ) if data not in collection else (True, None)
    return is_valid


def is_not_in(collection):
    def is_valid(data, detailed=False):
        if not detailed:
            return data not in collection
        return (
            False, 'data is not not in collection'
        ) if data in collection else (True, None)
    return is_valid


def is_none(data, detailed=False):
    if not detailed:
        return data is None
    return (False, 'data is not None') if data is not None else (True, None)


def is_not_none(data, detailed=False):
    if not detailed:
        return data is not None
    return (False, 'data is not not None') if data is None else (True, None)


def is_null(data, detailed=False):
    if not detailed:
        return data is None
    return (False, 'data is not null') if data is not None else (True, None)


def is_not_null(data, detailed=False):
    if not detailed:
        return data is not None
    return (False, 'data is not not null') if data is None else (True, None)


def is_match(regexp, flags=0):
    if isinstance(regexp, str):
        regexp = re.compile(regexp, flags=flags)
    rep = '/{}/{}'.format(regexp.pattern, ''.join(char for flag, char in [
        (re.A, 'a'), (re.I, 'i'), (re.L, 'l'),
        (re.M, 'm'), (re.S, 's'), (re.X, 'x'),
    ] if regexp.flags & flag))

    def is_valid(data, detailed=False):
        valid, errors = is_str(data, detailed=True)
        if not valid:
            return (False, errors) if detailed else False
        if regexp.match(data):
            return (True, None) if detailed else True
        return (
            False, 'data does not match {}'.format(rep)
        ) if detailed else False
    return is_valid


def is_not_match(regexp, flags=0):
    if isinstance(regexp, str):
        regexp = re.compile(regexp, flags=flags)
    rep = '/{}/{}'.format(regexp.pattern, ''.join(char for flag, char in [
        (re.A, 'a'), (re.I, 'i'), (re.L, 'l'),
        (re.M, 'm'), (re.S, 's'), (re.X, 'x'),
    ] if regexp.flags & flag))

    def is_valid(data, detailed=False):
        valid, errors = is_str(data, detailed=True)
        if not valid:
            return (False, errors) if detailed else False
        if not regexp.match(data):
            return (True, None) if detailed else True
        return (
            False, 'data does not not match {}'.format(rep)
        ) if detailed else False
    return is_valid
