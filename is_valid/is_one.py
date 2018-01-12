from .base import Predicate
from .explanation import Explanation
from .is_eq import is_eq


class is_one(Predicate):
    """
    Generates a predicate that will consider data valid if and only if exactly
    one of the given predicates considers the data valid.
    """

    def __init__(self, *predicates):
        self._predicates = [
            is_eq(predicate) if not callable(predicate) else predicate
            for predicate in predicates
        ]

    def _evaluate_explain(self, data):
        reasons, errors = [], []
        for predicate in self._predicates:
            explanation = predicate.explain(data)
            (reasons if explanation else errors).append(explanation)
        return Explanation(
            True, 'one_holds',
            'Exactly one of the given predicates hold.',
            reasons[0],
         ) if len(reasons) == 1 else Explanation(
            False, 'none_hold',
            'None of the given predicates hold.',
            errors,
         ) if len(reasons) == 0 else Explanation(
             False, 'multiple_hold',
            'Multiple of the given predicates hold.',
            reasons,
         )

    def _evaluate_no_explain(self, data):
        one = False
        for predicate in self._predicates:
            if predicate(data):
                if one:
                    return False
                one = True
        return one
