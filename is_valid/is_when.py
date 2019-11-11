from .base import Predicate
from .to_pred import to_pred
from .is_something import is_something
from .is_nothing import is_nothing


class is_when(Predicate):

    def __init__(self, value, then=is_something, else_=is_nothing):
        self._value = value
        self._then = to_pred(then)
        self._else = to_pred(else_)

    def _evaluate(self, data, explain, context):
        if context(self._value):
            return self._then(data, explain, context)
        else:
            return self._else(data, explain, context)

    @classmethod
    def cases(cls, *cases, default=is_nothing):
        predicate = to_pred(default)
        for cond, then_ in reversed(cases):
            predicate = cls(cond, then_, predicate)
        return predicate
