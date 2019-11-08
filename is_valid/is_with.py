from .base import Predicate
from .is_fixed import is_fixed
from .to_pred import to_pred


def to_func(value):
    if callable(value):
        return value

    def function(*args, **kwargs):
        return value

    return function


def dict_to_func(context):
    context = {
        key: to_func(value)
        for key, value in context.items()
    }

    def func(*args, **kwargs):
        return {
            key: func(*args, **kwargs)
            for key, func in context.items()
        }

    return func


class is_with(Predicate):
    """
    A predicate that can set context that can then be retrieved using Get
    objects.
    """

    fail = is_fixed(False, 'set_failed', 'failed to set context')

    def __init__(self, context, success, fail=fail):
        if isinstance(context, dict):
            context = dict_to_func(context)
        self._context = to_func(context)
        self._success = to_pred(success)
        self._fail = to_pred(fail)

    def _get_subject(self, data, context):
        return data

    def _evaluate(self, data, explain, context):
        try:
            values = self._context(self._get_subject(data, context))
        except Exception:
            return self._fail(data, explain, context)
        else:
            for key, value in values.items():
                context.push(key, value)
            res = self._success(data, explain, context)
            for key in values:
                context.pop(key)
            return res
