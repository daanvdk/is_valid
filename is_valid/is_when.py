from .base import Predicate
from .to_pred import to_pred
from .is_something import is_something
from .is_nothing import is_nothing


class is_when(Predicate):

    def __init__(self, value, pred=True, then=is_something, else_=is_nothing):
        self._value = value
        self._pred = to_pred(pred)
        self._then = to_pred(then)
        self._else = to_pred(else_)

    def _evaluate(self, data, explain, context):
        value = context(self._value)
        if self._pred(value, False, context):
            return self._then(data, explain, context)
        else:
            return self._else(data, explain, context)
