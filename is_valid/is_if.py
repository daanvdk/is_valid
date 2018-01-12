from .base import Predicate
from .is_eq import is_eq


class is_if(Predicate):
    """
    Generates a predicate that given a predicate as condition will based on the
    result of this condition on the data evaluate the data with either
    ``if_predicate`` or ``else_predicate``. If else predicate is omitted it
    will use the value of ``else_valid`` for when the condition considers the
    data invalid, as explanation it will reuse the explanation that the
    condition returned.
    """

    def __init__(
        self, condition, if_predicate, else_predicate=None, else_valid=True
    ):
        self._cond = condition if callable(condition) else is_eq(condition)
        self._if = (
            if_predicate
            if callable(if_predicate) else
            is_eq(if_predicate)
        )
        self._else = (
            else_predicate
            if else_predicate is None or callable(else_predicate) else
            is_eq(else_predicate)
        )
        self._else_valid = else_valid

    def _evaluate(self, data, explain):
        res = self._cond(data, explain and self._else is None)
        if res:
            return self._if(data, explain)
        if self._else is not None:
            return self._else(data, explain)
        if self._else_valid:
            res = ~res if explain else not res
        return res
