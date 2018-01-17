from .base import Predicate
from .explanation import Explanation
from .is_eq import to_pred
from .is_dict import is_dict


class is_subdict_where(Predicate):
    """
    Generates a predicate that checks that the data is a dict where for every
    key the value corresponding to that key is valid according to the given
    predicate corresponding to that key. If not all of the keys in the data
    have a corresponding predicate the data is considered invalid.

    The arguments for this function work exactly the same as that of the dict
    constructor.
    """

    prerequisites = [is_dict]

    _extra_exp = Explanation(False, 'not_allowed', 'Key is not allowed.')

    def __init__(self, *args, **kwargs):
        self._predicates = {
            key: to_pred(predicate)
            for key, predicate in dict(*args, **kwargs).items()
        }

    def _evaluate(self, data, explain, context):
        evaluate = set(data) & set(self._predicates)
        extra = set(data) - set(self._predicates)
        if not explain:
            return not extra and all(
                self._predicates[key](data[key], context=context)
                for key in evaluate
            )
        reasons, errors = {}, {}
        for key in evaluate:
            explanation = self._predicates[key].explain(data[key], context)
            (reasons if explanation else errors)[key] = explanation
        for key in extra:
            errors[key] = self._extra_exp
        return Explanation(
            True, 'subdict_where',
            'Data is a subdict where all the given predicates hold.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_subdict_where',
            'Data is not a subdict where all the given predicates hold.',
            errors,
        )
