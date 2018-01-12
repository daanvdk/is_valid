from .base import Predicate
from .is_eq import is_eq


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
        if not callable(predicate):
            predicate = is_eq(predicate)
        self._predicate = predicate

    def _evaluate(self, data, explain):
        return (
            ~self._predicate.explain(data)
            if explain else
            not self._predicate(data)
        )
