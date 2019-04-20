from .base import Predicate
from .explanation import Explanation
from .to_pred import to_pred
from .is_iterable import is_iterable


class is_iterable_where(Predicate):
    """
    Generates a predicate that checks that the data is an iterable where
    the 1st element of the data is valid according to the 1st given predicate,
    the 2nd element of the data is valid according to the 2nd given predicate
    and so on. Also requires that the amount of elements in the iterable is
    equal to the amount of predicates given.
    """

    prerequisites = [is_iterable]

    _overflow_exp = Explanation(False, 'overflow', 'data is overflowing')
    _missing_exp = Explanation(False, 'missing', 'data is missing')

    def __init__(self, *predicates):
        self._predicates = [to_pred(predicate) for predicate in predicates]

    def _evaluate(self, data, explain, context):
        data = list(data)
        if not explain:
            return len(data) == len(self._predicates) and all(
                predicate(value, context=context)
                for predicate, value in zip(self._predicates, data)
            )

        reasons = {}
        errors = {}
        new_data = []
        for i, (predicate, value) in enumerate(zip(self._predicates, data)):
            explanation = predicate.explain(value, context)
            if explanation:
                reasons[i] = explanation
            else:
                errors[i] = explanation
            new_data.append(explanation.data)
        for i in range(len(self._predicates), len(data)):
            errors[i] = self._overflow_exp
        for i in range(len(data), len(self._predicates)):
            errors[i] = self._missing_exp

        if errors:
            explanation = Explanation(
                False, 'not_iterable_where',
                'not all elements are valid according to their respective '
                'predicate',
                errors,
            )
        else:
            explanation = Explanation(
                True, 'iterable_where',
                (
                    'all elements are valid according to their respective '
                    'predicate'
                ),
                reasons,
            )
        explanation.data = new_data
        return explanation
