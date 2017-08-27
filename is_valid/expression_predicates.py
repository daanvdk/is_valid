import re

from .condition_predicates import is_all
from .base_predicates import is_not
from .type_predicates import is_str


def is_eq(value, rep=None):
    """
    Generates a predicate that checks if the data is equal to the given value.
    The optional keyword argument ``rep`` specifies what the value should be
    called in the explanation. If no value for ``rep`` is given it will just
    use ``repr(value)``.
    """
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
    """
    Generates a predicate that checks if the data is not equal to the given
    value. The optional keyword argument ``rep`` specifies what the value
    should be called in the explanation. If no value for ``rep`` is given it
    will just use ``repr(value)``.
    """
    return is_not(is_eq(value, rep=rep))


def is_gt(value, rep=None):
    """
    Generates a predicate that checks if the data greater than the given value.
    The optional keyword argument ``rep`` specifies what the value should be
    called in the explanation. If no value for ``rep`` is given it will just
    use ``repr(value)``.
    """
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
    """
    Generates a predicate that checks if the data greater than or equal to the
    given value. The optional keyword argument ``rep`` specifies what the value
    should be called in the explanation. If no value for ``rep`` is given it
    will just use ``repr(value)``.
    """
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
    """
    Generates a predicate that checks if the data lower than the given value.
    The optional keyword argument ``rep`` specifies what the value should be
    called in the explanation. If no value for ``rep`` is given it will just
    use ``repr(value)``.
    """
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
    """
    Generates a predicate that checks if the data lower than or equal to the
    given value. The optional keyword argument ``rep`` specifies what the value
    should be called in the explanation. If no value for ``rep`` is given it
    will just use ``repr(value)``.
    """
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
    """
    Generates a predicate that checks if the data is within the range specified
    by ``start`` and ``stop``. The optional arguments ``start_in`` and
    ``stop_in`` specify whether respectively ``start`` and ``stop`` should be
    included or excluded from the range.
    """
    return is_all(
        (is_geq if start_in else is_gt)(start),
        (is_leq if stop_in else is_lt)(stop)
    )


def is_in(collection):
    """
    Generates a predicate that checks if the data is within the given
    collection.
    """
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
    """
    A predicate that checks if the data is None.
    """
    if not explain:
        return data is None
    return (
        True, 'data is none'
    ) if data is None else (
        False, 'data is not none'
    )


def is_null(data, explain=False):
    """
    A predicate that checks if the data is None. Differs from
    ``is_none`` in it's explanation. This predicate will use the word `null` in
    it's explanation instead of `none`.
    """
    if not explain:
        return data is None
    return (
        True, 'data is null'
    ) if data is None else (
        False, 'data is not null'
    )


def is_match(pattern, flags=0):
    """
    A predicate that checks if the data matches the given pattern. If a string
    is provided as a pattern this predicate will compile it first. The
    optional parameter ``flags`` allows you to specify flags for this
    aforementioned compilation.
    """
    regexp = (
        re.compile(pattern, flags=flags)
    ) if isinstance(pattern, str) else pattern
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
