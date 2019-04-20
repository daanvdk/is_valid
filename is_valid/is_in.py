from .base import Predicate
from .explanation import Explanation


class is_in(Predicate):
    """
    Generates a predicate that checks if the data is within the given
    collection.
    """

    def __init__(self, collection, rep='the collection'):
        self._collection = collection
        self._valid_exp = Explanation(
            True, 'in_collection',
            'data is in {}'.format(rep)
        )
        self._not_valid_exp = Explanation(
            False, 'not_in_collection',
            'data is not in {}'.format(rep)
        )

    def _evaluate(self, data, explain, context):
        return (
            (self._valid_exp if explain else True)
            if data in context(self._collection) else
            (self._not_valid_exp if explain else False)
        )
