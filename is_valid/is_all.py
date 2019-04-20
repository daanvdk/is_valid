from .base import Predicate
from .explanation import Explanation
from .to_pred import to_pred


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
            else:
                self._predicates.append(to_pred(predicate))

    def _evaluate_explain(self, data, context):
        reasons, errors = [], []
        for predicate in self._predicates:
            explanation = predicate.explain(data, context)
            (reasons if explanation else errors).append(explanation)
        return Explanation(
            True, 'all_hold',
            'all of the given predicates hold',
            reasons,
        ) if not errors else Explanation(
            False, 'not_all_hold',
            'at least one of the given predicates does not hold',
            errors,
        )

    def _evaluate_no_explain(self, data, context):
        return all(
            predicate(data, context=context)
            for predicate in self._predicates
        )
