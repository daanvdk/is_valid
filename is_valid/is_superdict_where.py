from .base import Predicate
from .explanation import Explanation
from .is_eq import is_eq
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

    def __init__(self, *args, **kwargs):
        self._predicates = {
            key: predicate if callable(predicate) else is_eq(predicate)
            for key, predicate in dict(*args, **kwargs).items()
        }

    def _evaluate(self, data, explain):
        missing = set(self._predicates) - set(data)
        if missing:
            return Explanation(
                False, 'keys_incorrect',
                'The data keys do not follow the specification determined by'
                'the predicates.',
                {'missing': missing},
            ) if explain else False
        if not explain:
            return all(
                predicate(data[key])
                for key, predicate in self._predicates.items()
            )
        reasons, errors = {}, {}
        for key, predicate in self._predicates.items():
            explanation = predicate(data[key], explain=True)
            (reasons if explanation else errors)[key] = explanation
        return Explanation(
            True, 'superdict_where',
            'Data is a superdict where all the given predicates hold.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_superdict_where',
            'Data is not a superdict where all the given predicates hold.',
            errors,
        )
