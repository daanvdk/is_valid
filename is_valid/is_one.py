from .base import Predicate
from .explanation import Explanation
from .to_pred import to_pred


class is_one(Predicate):
    """
    Generates a predicate that will consider data valid if and only if exactly
    one of the given predicates considers the data valid.
    """

    def __init__(self, *predicates):
        self._predicates = [to_pred(predicate) for predicate in predicates]

    def _evaluate_explain(self, data, context):
        reasons, errors = [], []
        for predicate in self._predicates:
            explanation = predicate.explain(data, context)
            (reasons if explanation else errors).append(explanation)
        return Explanation(
            True, 'one_holds',
            'exactly one of the given predicates hold',
            reasons[0],
         ) if len(reasons) == 1 else Explanation(
            False, 'none_hold',
            'none of the given predicates hold',
            errors,
         ) if len(reasons) == 0 else Explanation(
             False, 'multiple_hold',
            'multiple of the given predicates hold',
            reasons,
         )

    def _evaluate_no_explain(self, data, context):
        one = False
        for predicate in self._predicates:
            if predicate(data, context=context):
                if one:
                    return False
                one = True
        return one
