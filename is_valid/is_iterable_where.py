from .base import Predicate
from .explanation import Explanation
from .is_eq import is_eq
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

    def __init__(self, *predicates):
        self._predicates = [
            predicate if callable(predicate) else is_eq(predicate)
            for predicate in predicates
        ]
        self._incorrect_length = Explanation(
            False, 'incorrect_length',
            'Data should have {} elements.'.format(len(predicates)),
        )

    def _evaluate(self, data, explain):
        data = list(data)
        if len(data) != len(self._predicates):
            return self._incorrect_length if explain else False
        if not explain:
            return all(p(v) for p, v in zip(self._predicates, data))
        reasons, errors = {}, {}
        for i, (predicate, value) in enumerate(zip(self._predicates, data)):
            explanation = predicate.explain(value)
            (reasons if explanation else errors)[i] = explanation
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
