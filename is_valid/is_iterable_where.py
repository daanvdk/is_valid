from .base import Predicate
from .explanation import Explanation
from .is_eq import to_pred
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

    _overflow_exp = Explanation(False, 'overflow', 'Data is overflowing.')
    _missing_exp = Explanation(False, 'missing', 'Data is missing.')

    def __init__(self, *predicates):
        self._predicates = [to_pred(predicate) for predicate in predicates]

    def _evaluate(self, data, explain, context):
        data = list(data)
        if not explain:
            return len(data) == len(self._predicates) and all(
                predicate(value, context=context)
                for predicate, value in zip(self._predicates, data)
            )
        reasons, errors = {}, {}
        for i, (predicate, value) in enumerate(zip(self._predicates, data)):
            explanation = predicate.explain(value, context)
            (reasons if explanation else errors)[i] = explanation
        for i in range(len(reasons) + len(errors), len(data)):
            errors[i] = self._overflow_exp
        for i in range(len(reasons) + len(errors), len(self._predicates)):
            errors[i] = self._missing_exp
        return Explanation(
            True, 'all_valid',
            'All elements are valid according to their respective predicate.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_all_valid',
            'Not all elements are valid according to their respective '
            'predicate.',
            errors,
        )
