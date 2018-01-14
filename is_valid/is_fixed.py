from .base import Predicate
from .explanation import Explanation


class is_fixed(Predicate):
    """
    Generates a predicate that returns a certain value for valid, code, and
    message that it will always return regardless of what data you put into
    it.
    """

    def __init__(self, valid, code, message, details=None):
        self._valid = valid
        self._explanation = Explanation(valid, code, message, details)

    def _evaluate(self, data, explain, context):
        return self._explanation if explain else self._valid
