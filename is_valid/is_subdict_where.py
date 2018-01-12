from .base import Predicate
from .explanation import Explanation
from .is_eq import is_eq
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

    def __init__(self, *args, **kwargs):
        self._predicates = {
            key: predicate if callable(predicate) else is_eq(predicate)
            for key, predicate in dict(*args, **kwargs).items()
        }

    def _evaluate(self, data, explain):
        extra = set(data) - set(self._predicates)
        if extra:
            return Explanation(
                False, 'keys_incorrect',
                'The data keys do not follow the specification determined by'
                'the predicates.',
                {'extra': extra},
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
            True, 'subdict_where',
            'Data is a subdict where all the given predicates hold.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_subdict_where',
            'Data is not a subdict where all the given predicates hold.',
            errors,
        )
