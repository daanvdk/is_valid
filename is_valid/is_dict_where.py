from collections import defaultdict

from .base import Predicate
from .explanation import Explanation
from .to_pred import to_pred
from .is_dict import is_dict
from .is_fixed import is_fixed


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

    _missing_exp = Explanation(False, 'missing', 'key is missing')
    _extra_pred = is_fixed(False, 'not_allowed', 'key is not allowed')

    def __init__(self, *args, **kwargs):
        self._predicates = defaultdict(lambda: self._extra_pred)

        if len(args) == 2 and len(kwargs) == 0:
            self._required = set(args[0])
            self._predicates.update(
                (key, to_pred(predicate))
                for key, predicate in args[0].items()
            )
            self._predicates.update(
                (key, to_pred(predicate))
                for key, predicate in args[1].items()
            )
        else:
            predicates = dict(*args, **kwargs)
            self._required = set(predicates)
            self._predicates.update(
                (key, to_pred(predicate))
                for key, predicate in predicates.items()
            )

    def _evaluate(self, data, explain, context):
        missing = {key for key in self._required if key not in data}

        if not explain:
            return not missing and all(
                self._predicates[key](value, context=context)
                for key, value in data.items()
            )

        reasons = {}
        errors = {}
        new_data = {}

        for key, value in data.items():
            explanation = self._predicates[key].explain(value, context)
            if explanation:
                reasons[key] = explanation
            else:
                errors[key] = explanation
            new_data[key] = explanation.data
        for key in missing:
            errors[key] = self._missing_exp

        if errors:
            explanation = Explanation(
                False, 'not_dict_where',
                'data is not a dict where all the given predicates hold',
                errors,
            )
        else:
            explanation = Explanation(
                True, 'dict_where',
                'data is a dict where all the given predicates hold',
                reasons,
            )
        explanation.data = new_data
        return explanation
