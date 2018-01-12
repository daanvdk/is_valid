from .base import Predicate
from .explanation import Explanation
from .is_eq import is_eq


class is_object_where(Predicate):
    """
    Generates a predicate that checks that the data is an object where every
    given predicate holds for the associated attribute on the object.
    """

    _no_such_attr = Explanation(
        False, 'no_such_attr',
        'Data does not have this attribute.',
    )

    def __init__(self, *args, **kwargs):
        self._predicates = {
            attr: predicate if callable(predicate) else is_eq(predicate)
            for attr, predicate in dict(*args, **kwargs).items()
        }

    def _evaluate_explain(self, data):
        reasons, errors = {}, {}
        for attr, predicate in self._predicates.items():
            if hasattr(data, attr):
                explanation = predicate(getattr(data, attr), explain=True)
                (reasons if explanation else errors)[attr] = explanation
            else:
                errors[attr] = self._no_such_attr
        return Explanation(
            True, 'object_where',
            'Data is an object where all the given predicates hold.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_object_where',
            'Data is not an object where all the given predicates hold.',
            errors,
        )

    def _evaluate_no_explain(self, data):
        return all(
            hasattr(data, attr) and predicate(getattr(data, attr))
            for attr, predicate in self._predicates.items()
        )
