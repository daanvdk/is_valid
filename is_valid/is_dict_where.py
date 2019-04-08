from .base import Predicate
from .explanation import Explanation
from .to_pred import to_pred
from .is_dict import is_dict


class is_dict_where(Predicate):
    """
    Generates a predicate that checks that the data is a dict where for every
    key the value corresponding to that key is valid according to the given
    predicate corresponding to that key. If the keys of the data and the keys
    of the given predicates do not match the data is considered invalid.

    The arguments for this function work exactly the same as that of the dict
    constructor.
    """

    prerequisites = [is_dict]

    _missing_exp = Explanation(False, 'missing', 'Key is missing')
    _extra_exp = Explanation(False, 'not_allowed', 'Key is not allowed.')

    def __init__(self, *args, **kwargs):
        if len(args) == 2 and len(kwargs) == 0:
            self._required = {
                key: to_pred(predicate)
                for key, predicate in args[0].items()
            }
            self._optional = {
                key: to_pred(predicate)
                for key, predicate in args[1].items()
            }
        else:
            self._required = {
                key: to_pred(predicate)
                for key, predicate in dict(*args, **kwargs).items()
            }
            self._optional = {}

        self._predicates = dict(self._optional)
        self._predicates.update(self._required)

    def _evaluate(self, data, explain, context):
        evaluate = set(data) & set(self._predicates)
        missing = set(self._required) - set(data)
        extra = set(data) - set(self._required) - set(self._optional)
        if not explain:
            return not extra and not missing and all(
                self._predicates[key](data[key], context=context)
                for key in evaluate
            )
        reasons, errors = {}, {}
        for key in evaluate:
            explanation = self._predicates[key].explain(data[key], context)
            (reasons if explanation else errors)[key] = explanation
        for key in missing:
            errors[key] = self._missing_exp
        for key in extra:
            errors[key] = self._extra_exp
        return Explanation(
            True, 'dict_where',
            'Data is a dict where all the given predicates hold.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_dict_where',
            'Data is not a dict where all the given predicates hold.',
            errors,
        )
