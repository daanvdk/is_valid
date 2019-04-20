from .base import Predicate
from .explanation import Explanation
from .to_pred import to_pred


class is_object_where(Predicate):
    """
    Generates a predicate that checks that the data is an object where every
    given predicate holds for the associated attribute on the object.
    """

    _no_such_attr = Explanation(
        False, 'no_such_attr',
        'Data does not have this attribute',
    )

    def __init__(self, *args, **kwargs):
        self._predicates = {
            attr: to_pred(predicate)
            for attr, predicate in dict(*args, **kwargs).items()
        }

    def _evaluate_explain(self, data, context):
        reasons, errors = {}, {}
        for attr, predicate in self._predicates.items():
            if hasattr(data, attr):
                explanation = predicate.explain(getattr(data, attr), context)
                (reasons if explanation else errors)[attr] = explanation
            else:
                errors[attr] = self._no_such_attr
        return Explanation(
            True, 'object_where',
            'data is an object where all the given predicates hold',
            reasons,
        ) if not errors else Explanation(
            False, 'not_object_where',
            'data is not an object where all the given predicates hold',
            errors,
        )

    def _evaluate_no_explain(self, data, context):
        return all(
            hasattr(data, attr) and
            predicate(getattr(data, attr), context=context)
            for attr, predicate in self._predicates.items()
        )
