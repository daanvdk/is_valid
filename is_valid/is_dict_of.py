from .base import Predicate
from .explanation import Explanation
from .is_eq import is_eq
from .is_iterable import is_iterable


class is_dict_of(Predicate):
    """
    Generates a predicate that checks that the data is a dict where every key
    is valid according to ``key_predicate`` and every value is valid according
    to ``val_predicate``.
    """

    prerequisites = [is_iterable]

    def __init__(self, key_predicate, value_predicate):
        if not callable(key_predicate):
            key_predicate = is_eq(key_predicate)
        if not callable(value_predicate):
            value_predicate = is_eq(value_predicate)
        self._key = key_predicate
        self._value = value_predicate

    def _evaluate_explain(self, data):
        reasons, errors = {}, {}
        for key, value in data.items():
            reason, error = {}, {}
            explanation = self._key.explain(key)
            (reason if explanation else error)['key'] = explanation
            explanation = self._value.explain(value)
            (reason if explanation else error)['value'] = explanation
            if error:
                errors[key] = error
            else:
                reasons[key] = reason
        return Explanation(
            True, 'all_valid',
            'All elements are valid according to the predicate.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_all_valid',
            'Not all elements are valid according to the predicate.',
            errors,
        )

    def _evaluate_no_explain(self, data):
        return all(
            self._key(key) and self._value(value)
            for key, value in data.items()
        )
