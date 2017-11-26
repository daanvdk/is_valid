import re

from .explanation import Explanation
from .utils import explain
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
    return explain(
        lambda data: data == value,
        'equal_to',
        'Data is equal to {}.'.format(rep),
        'Data is not equal to {}.'.format(rep),
    )


def is_gt(value, rep=None):
    """
    Generates a predicate that checks if the data greater than the given value.
    The optional keyword argument ``rep`` specifies what the value should be
    called in the explanation. If no value for ``rep`` is given it will just
    use ``repr(value)``.
    """
    if rep is None:
        rep = repr(value)
    return explain(
        lambda data: data > value,
        'greater_than',
        'Data is greater than {}.'.format(rep),
        'Data is not greater than {}.'.format(rep),
    )


def is_geq(value, rep=None):
    """
    Generates a predicate that checks if the data greater than or equal to the
    given value. The optional keyword argument ``rep`` specifies what the value
    should be called in the explanation. If no value for ``rep`` is given it
    will just use ``repr(value)``.
    """
    if rep is None:
        rep = repr(value)
    return explain(
        lambda data: data >= value,
        'greater_than_or_equal_to',
        'Data is greater than or equal to {}.'.format(rep),
        'Data is not greater than or equal to {}.'.format(rep),
    )


def is_lt(value, rep=None):
    """
    Generates a predicate that checks if the data is lower than the given
    value. The optional keyword argument ``rep`` specifies what the value
    should be called in the explanation. If no value for ``rep`` is given it
    will just use ``repr(value)``.
    """
    if rep is None:
        rep = repr(value)
    return explain(
        lambda data: data < value,
        'lower_than',
        'Data is lower than {}.'.format(rep),
        'Data is not lower than {}.'.format(rep),
    )


def is_leq(value, rep=None):
    """
    Generates a predicate that checks if the data lower than or equal to the
    given value. The optional keyword argument ``rep`` specifies what the value
    should be called in the explanation. If no value for ``rep`` is given it
    will just use ``repr(value)``.
    """
    if rep is None:
        rep = repr(value)
    return explain(
        lambda data: data <= value,
        'lower_than_or_equal_to',
        'Data is lower than or equal to {}.'.format(rep),
        'Data is not lower than or equal to {}.'.format(rep),
    )


def is_in_range(
    start, stop, start_in=True, stop_in=False, start_rep=None, stop_rep=None
):
    """
    Generates a predicate that checks if the data is within the range specified
    by ``start`` and ``stop``. The optional arguments ``start_in`` and
    ``stop_in`` specify whether respectively ``start`` and ``stop`` should be
    included or excluded from the range.
    """
    if start_rep is None:
        start_rep = repr(start_rep)
    if stop_rep is None:
        stop_rep = repr(stop_rep)

    start_predicate = (is_geq if start_in else is_gt)(start, rep=start_rep)
    stop_predicate = (is_leq if stop_in else is_lt)(stop, rep=stop_rep)

    def is_valid(data, explain=False):
        if not explain:
            return start_predicate(data) and stop_predicate(data)
        start_explanation = start_predicate(data, explain=True)
        if not start_explanation:
            return start_explanation
        stop_explanation = stop_predicate(data, explain=True)
        if not stop_explanation:
            return stop_explanation
        return Explanation(
            True, 'in_range',
            start_explanation.message[:-1] + ' and ' +
            stop_explanation.message[9:],
        )
    return is_valid


def is_in(collection):
    """
    Generates a predicate that checks if the data is within the given
    collection.
    """
    return explain(
        lambda data: data in collection,
        'in_collection',
        'Data is contained within the collection.',
        'Data is not contained within the collection.',
    )


#: A predicate that checks if the data is None.
is_none = explain(
    lambda data: data is None,
    'none', 'Data is None.', 'Data is not None.',
)
#: A predicate that checks if the data is None. Differs from ``is_none`` in
#: it's explanation. This predicate will use the word `null` in it's
#: explanation instead of `None`.
is_null = explain(
    lambda data: data is None,
    'null', 'Data is null.', 'Data is not null.',
)


def is_match(regexp, flags=0, rep=None):
    """
    A predicate that checks if the data matches the given pattern. If a string
    is provided as a pattern this predicate will compile it first. The
    optional parameter ``flags`` allows you to specify flags for this
    aforementioned compilation.
    """
    if isinstance(regexp, str):
        regexp = re.compile(regexp, flags=flags)
    if rep is None:
        rep = '/{}/{}'.format(
            regexp.pattern,
            ''.join(char for flag, char in [
                (re.A, 'a'), (re.I, 'i'), (re.L, 'l'),
                (re.M, 'm'), (re.S, 's'), (re.X, 'x'),
            ] if regexp.flags & flag)
        )

    def is_valid(data, explain=False):
        res = is_str(data, explain=explain)
        if not res:
            return res
        if not explain:
            return bool(regexp.match(data))
        return Explanation(
            True, 'match', 'Data does match {}.'.format(rep),
        ) if regexp.match(data) else Explanation(
            False, 'not_match', 'Data does not match {}.'.format(rep),
        )
    return is_valid
