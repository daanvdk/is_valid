from .base import Predicate
from .explanation import Explanation
from .to_pred import to_pred


class is_any(Predicate):
    """
    Generates a predicate that will consider data valid if and only if any of
    the given predicates considers the data valid.
    """

    def __init__(self, *predicates):
        self._predicates = []
        for predicate in predicates:
            if isinstance(predicate, is_any):
                self._predicates.extend(predicate._predicates)
            else:
                self._predicates.append(to_pred(predicate))

    def _evaluate_explain(self, data, context):
        reasons, errors = [], []
        for predicate in self._predicates:
            explanation = predicate.explain(data, context)
            (reasons if explanation else errors).append(explanation)
        return Explanation(
            True, 'any_holds',
            'at least one of the given predicates holds',
            reasons,
        ) if reasons else Explanation(
            False, 'not_any_holds',
            'none of the given predicates holds',
            errors,
        )

    def _evaluate_no_explain(self, data, context):
        return any(
            predicate(data, context=context)
            for predicate in self._predicates
        )
