from .base import Predicate
from .explanation import Explanation


class is_eq(Predicate):
    """
    Generates a predicate that checks if the data is equal to the given value.
    The optional keyword argument ``rep`` specifies what the value should be
    called in the explanation. If no value for ``rep`` is given it will just
    use ``repr(value)``.
    """

    def __init__(self, value, rep=None):
        if rep is None:
            rep = repr(value)
        self._value = value
        self._valid_exp = Explanation(
            True, 'equal_to', 'Data is equal to {}'.format(rep)
        )
        self._not_valid_exp = Explanation(
            False, 'not_equal_to', 'Data is not equal to {}'.format(rep)
        )

    def _evaluate(self, data, explain, context):
        return (
            (self._valid_exp if explain else True)
            if data == context(self._value) else
            (self._not_valid_exp if explain else False)
        )


def to_pred(value):
    if isinstance(value, Predicate):
        return value
    elif isinstance(value, dict):
        from .is_dict_where import is_dict_where
        return is_dict_where(value)
    elif isinstance(value, list):
        from .is_list_where import is_list_where
        return is_list_where(*value)
    elif isinstance(value, tuple):
        from .is_tuple_where import is_tuple_where
        return is_tuple_where(*value)
    else:
        return is_eq(value)
