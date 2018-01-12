from .base import Predicate
from .is_null import is_null
from .is_eq import is_eq


class is_nullable(Predicate):

    def __init__(self, predicate):
        if not callable(predicate):
            predicate = is_eq(predicate)
        self._predicate = predicate

    def _evaluate(self, data, explain):
        res = is_null(data, explain)
        if res:
            return res
        return self._predicate(data, explain)
