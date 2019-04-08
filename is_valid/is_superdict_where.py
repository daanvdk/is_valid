from .base import Predicate
from .explanation import Explanation
from .to_pred import to_pred
from .is_dict import is_dict


class is_superdict_where(Predicate):
    """
    Generates a predicate that checks that the data is a dict where for every
    key the value corresponding to that key is valid according to the given
    predicate corresponding to that key. If not all of the keys in the given
    predicates are in the data the data is considered invalid.

    The arguments for this function work exactly the same as that of the dict
    constructor.
    """

    prerequisites = [is_dict]

    _missing_exp = Explanation(False, 'missing', 'Key is missing')

    def __init__(self, *args, **kwargs):
        self._predicates = {
            key: to_pred(predicate)
            for key, predicate in dict(*args, **kwargs).items()
        }

    def _evaluate(self, data, explain, context):
        evaluate = set(data) & set(self._predicates)
        missing = set(self._predicates) - set(data)
        if not explain:
            return not missing and all(
                self._predicates[key](data[key], context=context)
                for key in evaluate
            )
        reasons, errors = {}, {}
        for key in evaluate:
            explanation = self._predicates[key].explain(data[key])
            (reasons if explanation else errors)[key] = explanation
        for key in missing:
            errors[key] = self._missing_exp
        return Explanation(
            True, 'superdict_where',
            'Data is a superdict where all the given predicates hold.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_superdict_where',
            'Data is not a superdict where all the given predicates hold.',
            errors,
        )
