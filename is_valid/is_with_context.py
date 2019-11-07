from .base import Predicate
from .is_fixed import is_fixed
from .to_pred import to_pred


def const(value):
    def function(*args, **kwargs):
        return value
    return function


class is_with_context(Predicate):
    """
    A predicate that can set context that can then be retrieved using Get
    objects.
    """

    fail = is_fixed(False, 'set_failed', 'failed to set context')

    def __init__(self, context, success, fail=fail):
        self._context = {
            key: transform if callable(transform) else const(transform)
            for key, transform in context.items()
        }
        self._success = to_pred(success)
        self._fail = to_pred(fail)

    def _evaluate(self, data, explain, context):
        context_values = {
            key: values[-1]
            for key, values in context._values.items()
        }
        try:
            values = {
                key: transform(context_values)
                for key, transform in self._context.items()
            }
        except Exception:
            return self._fail(data, explain, context)
        else:
            for key, value in values.items():
                context.push(key, value)
            res = self._success(data, explain, context)
            for key in values:
                context.pop(key)
            return res
