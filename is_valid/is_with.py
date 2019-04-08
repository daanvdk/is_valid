from .base import Predicate
from .is_fixed import is_fixed
from .to_pred import to_pred


class is_with(Predicate):
    """
    A predicate that can set context that can then be retrieved using Get
    objects.
    """

    fail = is_fixed(False, 'set_failed', 'Failed to set context.')

    def __init__(self, context, success, fail=fail):
        self._context = context
        self._success = to_pred(success)
        self._fail = to_pred(fail)

    def _evaluate(self, data, explain, context):
        try:
            values = {
                key: transform(data)
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
