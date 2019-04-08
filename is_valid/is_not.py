from .base import Predicate
from .to_pred import to_pred


class is_not(Predicate):
    """
    Generates the inverse of a given predicate. So if the given predicate would
    consider the data valid the generated predicate will consider it invalid,
    and the other way around. It reuses the explanation of the given predicate.
    """

    def __new__(cls, predicate):
        if isinstance(predicate, is_not):
            return predicate._predicate
        return super().__new__(cls)

    def __init__(self, predicate):
        self._predicate = to_pred(predicate)

    def _evaluate(self, data, explain, context):
        return (
            ~self._predicate.explain(data, context)
            if explain else
            not self._predicate(data, context=context)
        )
