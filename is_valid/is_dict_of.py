from .base import Predicate
from .explanation import Explanation
from .to_pred import to_pred
from .is_dict import is_dict


class is_dict_of(Predicate):
    """
    Generates a predicate that checks that the data is a dict where every key
    is valid according to ``key_predicate`` and every value is valid according
    to ``val_predicate``.
    """

    prerequisites = [is_dict]

    def __init__(self, key_predicate, value_predicate):
        self._key = to_pred(key_predicate)
        self._value = to_pred(value_predicate)

    def _evaluate_explain(self, data, context):
        reasons, errors = {}, {}
        for key, value in data.items():
            reason, error = {}, {}
            explanation = self._key.explain(key, context)
            (reason if explanation else error)['key'] = explanation
            explanation = self._value.explain(value, context)
            (reason if explanation else error)['value'] = explanation
            if error:
                errors[key] = error
            else:
                reasons[key] = reason
        return Explanation(
            True, 'dict_of',
            'all elements are valid according to the predicate',
            reasons,
        ) if not errors else Explanation(
            False, 'not_dict_of',
            'not all elements are valid according to the predicate',
            errors,
        )

    def _evaluate_no_explain(self, data, context):
        return all(
            self._key(key, context=context) and
            self._value(value, context=context)
            for key, value in data.items()
        )
