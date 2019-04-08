from .base import Predicate
from .is_none import is_none
from .to_pred import to_pred


class is_optional(Predicate):

    def __init__(self, predicate):
        self._predicate = to_pred(predicate)

    def _evaluate(self, data, explain, context):
        res = is_none(data, explain, context)
        if res:
            return res
        return self._predicate(data, explain, context)
