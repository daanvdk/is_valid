from .base import Predicate
from .explanation import Explanation
from .to_pred import to_pred
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
        reasons = {}
        errors = {}
        new_data = []

        for i, value in enumerate(data):
            explanation = self._predicate.explain(value, context)
            if explanation:
                reasons[i] = explanation
            else:
                errors[i] = explanation
            new_data.append(explanation.data)

        if errors:
            explanation = Explanation(
                False, 'not_iterable_of',
                'not all elements are valid according to the predicate',
                errors,
            )
        else:
            explanation = Explanation(
                True, 'iterable_of',
                'all elements are valid according to the predicate',
                reasons,
            )
        explanation.data = new_data
        return explanation

    def _evaluate_no_explain(self, data, context):
        return all(
            self._predicate(value, context=context)
            for value in data
        )
