from .base import Predicate
from .is_null import is_null
from .is_eq import to_pred


class is_nullable(Predicate):

    def __init__(self, predicate):
        self._predicate = to_pred(predicate)

    def _evaluate(self, data, explain, context):
        res = is_null(data, explain, context)
        if res:
            return res
        return self._predicate(data, explain, context)
