from .base import Predicate
from .is_none import is_none
from .is_eq import is_eq


class is_optional(Predicate):

    def __init__(self, predicate):
        if not callable(predicate):
            predicate = is_eq(predicate)
        self._predicate = predicate

    def _evaluate(self, data, explain):
        res = is_none(data, explain)
        if res:
            return res
        return self._predicate(data, explain)
