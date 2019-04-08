from .base import Predicate
from .to_pred import to_pred


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
        self._cond = to_pred(condition)
        self._if = to_pred(if_predicate)
        self._else = (
            None if else_predicate is None else to_pred(else_predicate)
        )
        self._else_valid = else_valid

    def _evaluate(self, data, explain, context):
        res = self._cond(data, explain and self._else is None, context)
        if res:
            return self._if(data, explain, context)
        if self._else is not None:
            return self._else(data, explain, context)
        if self._else_valid:
            res = ~res if explain else not res
        return res
