from .base import Predicate
from .explanation import Explanation
from .is_eq import is_eq


class is_all(Predicate):
    """
    Generates a predicate that will consider data valid if and only if all of
    the given predicates considers the data valid.
    """

    def __init__(self, *predicates):
        self._predicates = []
        for predicate in predicates:
            if isinstance(predicate, is_all):
                self._predicates.extend(predicate._predicates)
            elif not callable(predicate):
                self._predicates.append(is_eq(predicate))
            else:
                self._predicates.append(predicate)

    def _evaluate_explain(self, data):
        reasons, errors = [], []
        for predicate in self._predicates:
            explanation = predicate.explain(data)
            (reasons if explanation else errors).append(explanation)
        return Explanation(
            True, 'all_hold',
            'All of the given predicates hold.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_all_hold',
            'At least one of the given predicates does not hold.',
            errors,
        )

    def _evaluate_no_explain(self, data):
        return all(predicate(data) for predicate in self._predicates)
