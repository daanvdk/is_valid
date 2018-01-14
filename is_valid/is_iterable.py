from .base import Predicate, instantiate
from .explanation import Explanation


@instantiate
class is_iterable(Predicate):
    """
    A predicate that checks if the data is iterable.
    """

    def __init__(self):
        self._valid_exp = Explanation(True, 'iterable', 'Data is iterable.')
        self._not_valid_exp = Explanation(
            False, 'not_iterable', 'Data is not iterable.'
        )

    def _evaluate(self, data, explain, context):
        try:
            iter(data)
        except TypeError:
            return self._not_valid_exp if explain else False
        else:
            return self._valid_exp if explain else True
