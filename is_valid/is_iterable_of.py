from .base import Predicate
from .explanation import Explanation
from .is_eq import to_pred
from .is_iterable import is_iterable


class is_iterable_of(Predicate):
    """
    Generates a predicate that checks that the data is an iterable where
    every element of the data is valid according to the given predicate.
    """

    prerequisites = [is_iterable]

    def __init__(self, predicate):
        self._predicate = to_pred(predicate)

    def _evaluate_explain(self, data, context):
        reasons, errors = {}, {}
        for i, value in enumerate(data):
            explanation = self._predicate.explain(value, context)
            (reasons if explanation else errors)[i] = explanation
        return Explanation(
            True, 'all_valid',
            'All elements are valid according to the predicate.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_all_valid',
            'Not all elements are valid according to the predicate.',
            errors,
        )

    def _evaluate_no_explain(self, data, context):
        return all(
            self._predicate(value, context=context)
            for value in data
        )
