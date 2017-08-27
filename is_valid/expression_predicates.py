import re

from .condition_predicates import is_all
from .base_predicates import is_not
from .type_predicates import is_str


def is_eq(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, explain=False):
        if not explain:
            return data == value
        return (
            True, 'data is equal to {}'.format(rep)
        ) if data == value else (
            False, 'data is not equal to {}'.format(rep)
        )
    return is_valid


def is_neq(value, rep=None):
    return is_not(is_eq(value, rep=rep))


def is_gt(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, explain=False):
        if not explain:
            return data > value
        return (
            True, 'data is greater than {}'.format(rep)
        ) if data > value else (
            False, 'data is not greater than {}'.format(rep)
        )
    return is_valid


def is_geq(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, explain=False):
        if not explain:
            return data >= value
        return (
            True, 'data is greater than or equal to {}'.format(rep)
        ) if data >= value else (
            False, 'data is not greater than or equal to {}'.format(rep)
        )
    return is_valid


def is_lt(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, explain=False):
        if not explain:
            return data < value
        return (
            True, 'data is lower than {}'.format(rep)
        ) if data < value else (
            False, 'data is not lower than {}'.format(rep)
        )
    return is_valid


def is_leq(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, explain=False):
        if not explain:
            return data <= value
        return (
            True, 'data is lower than or equal to {}'.format(rep)
        ) if data <= value else (
            False, 'data is not lower than or equal to {}'.format(rep)
        )
    return is_valid


def is_in_range(start, stop, start_in=True, stop_in=False):
    return is_all(
        (is_geq if start_in else is_gt)(start),
        (is_leq if stop_in else is_lt)(stop)
    )


def is_in(collection):
    def is_valid(data, explain=False):
        if not explain:
            return data in collection
        return (
            True, 'data is in collection'
        ) if data in collection else (
            False, 'data is not in collection'
        )
    return is_valid


def is_none(data, explain=False):
    if not explain:
        return data is None
    return (
        True, 'data is None'
    ) if data is None else (
        False, 'data is not None'
    )


def is_null(data, explain=False):
    if not explain:
        return data is None
    return (
        True, 'data is null'
    ) if data is None else (
        False, 'data is not null'
    )


def is_match(regexp, flags=0):
    if isinstance(regexp, str):
        regexp = re.compile(regexp, flags=flags)
    rep = '/{}/{}'.format(regexp.pattern, ''.join(char for flag, char in [
        (re.A, 'a'), (re.I, 'i'), (re.L, 'l'),
        (re.M, 'm'), (re.S, 's'), (re.X, 'x'),
    ] if regexp.flags & flag))

    def is_valid(data, explain=False):
        valid, errors = is_str(data, explain=True)
        if not valid:
            return (False, errors) if explain else False
        if not explain:
            return bool(regexp.match(data))
        return (
            True, 'data does match {}'.format(rep)
        ) if regexp.match(data) else (
            False, 'data does not match {}'.format(rep)
        )
    return is_valid
