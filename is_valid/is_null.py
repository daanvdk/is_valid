from .base import Predicate, instantiate
from .explanation import Explanation


@instantiate
class is_null(Predicate):
    """
    A predicate that checks if the data is None. Differs from ``is_none`` in
    it's explanation. This predicate will use the word `null` in it's
    explanation instead of `None`.
    """

    def __init__(self):
        self._valid_exp = Explanation(True, 'null', 'data is null')
        self._not_valid_exp = Explanation(
            False, 'not_null', 'data is not null'
        )

    def _evaluate(self, data, explain, context):
        return (
            (self._valid_exp if explain else True)
            if data is None else
            (self._not_valid_exp if explain else False)
        )
