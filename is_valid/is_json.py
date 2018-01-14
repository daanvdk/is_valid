from .base import Predicate, instantiate
from .explanation import Explanation
from json import loads


@instantiate
class is_json(Predicate):
    """
    A predicate that checks if the data is valid json.
    """

    def __init__(self):
        self._valid_exp = Explanation(True, 'json', 'Data is json.')
        self._not_valid_exp = Explanation(
            False, 'not_json', 'Data is not json.'
        )

    def _evaluate(self, data, explain, context):
        try:
            loads(data)
        except ValueError:
            return self._not_valid_exp if explain else False
        else:
            return self._valid_exp if explain else True
