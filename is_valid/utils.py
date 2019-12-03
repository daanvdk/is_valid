from .base import Predicate
from .explanation import Explanation
from .is_eq import is_eq
from .to_pred import to_pred
from .is_with_context import is_with_context


class explain(Predicate):
    """
    Wraps a predicate with an explanation. You can set the explanation messages
    with the parameters ``explanation_valid`` and ``explanation_invalid``.

    This method is also very nice way to use predicates from other sources than
    `Is Valid?` that don't have an ``explain`` parameter to work with
    explanations.
    """

    def __init__(
        self, predicate, code='valid',
        message_valid='data is valid', message_invalid='data is not valid',
        details_valid=None, details_invalid=None,
    ):
        if not callable(predicate):
            predicate = is_eq(predicate)
        self._context = isinstance(predicate, Predicate)
        self._predicate = predicate
        self._valid_exp = Explanation(
            True, code, message_valid, details_valid
        )
        self._not_valid_exp = Explanation(
            False, 'not_{}'.format(code), message_invalid, details_invalid
        )

    def _evaluate(self, data, explain, context):
        if self._context:
            valid = self._predicate(data, explain, context)
        else:
            valid = self._predicate(data)

        if explain:
            res = self._valid_exp if valid else self._not_valid_exp
            if self._context:
                res = res.copy()
                res.data = valid.data
            return res
        else:
            return bool(valid)


class Wrapper(Predicate):

    def __init__(self, wrapped=None):
        if wrapped is not None:
            wrapped = to_pred(wrapped)
        self._wrapped = wrapped

    def wrap(self, wrapped):
        wrapped = to_pred(wrapped)
        self._wrapped = wrapped
        return wrapped

    def _evaluate(self, data, explain, context):
        return self._wrapped(data, explain, context)


def default_context(pred, *args, **kwargs):
    """
    Wraps a predicate with default context.
    """
    defaults = dict(*args, **kwargs)

    def context_func(context):
        return {
            key: value
            for key, value in defaults.items()
            if key not in context
        }

    return is_with_context(context_func, pred)
