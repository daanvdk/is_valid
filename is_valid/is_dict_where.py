from .base import Predicate
from .explanation import Explanation
from .is_eq import is_eq
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

    def __init__(self, *args, **kwargs):
        if len(args) == 2 and len(kwargs) == 0:
            self._required = {
                key: predicate if callable(predicate) else is_eq(predicate)
                for key, predicate in args[0].items()
            }
            self._optional = {
                key: predicate if callable(predicate) else is_eq(predicate)
                for key, predicate in args[1].items()
            }
        else:
            self._required = {
                key: predicate if callable(predicate) else is_eq(predicate)
                for key, predicate in dict(*args, **kwargs).items()
            }
            self._optional = {}

        self._predicates = dict(self._optional)
        self._predicates.update(self._required)

    def _evaluate(self, data, explain):
        missing = set(self._required) - set(data)
        extra = set(data) - set(self._required) - set(self._optional)
        if missing or extra:
            return Explanation(
                False, 'keys_incorrect',
                'The data keys do not follow the specification determined by'
                'the predicates.',
                {k: v for k, v in {
                    'missing': missing,
                    'extra': extra,
                }.items() if v},
            ) if explain else False

        if not explain:
            return all(
                self._predicates[key](value)
                for key, value in data.items()
            )
        reasons, errors = {}, {}
        for key, value in data.items():
            explanation = self._predicates[key](value, explain=True)
            (reasons if explanation else errors)[key] = explanation
        return Explanation(
            True, 'dict_where',
            'Data is a dict where all the given predicates hold.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_dict_where',
            'Data is not a dict where all the given predicates hold.',
            errors,
        )
