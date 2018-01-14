from .base import Predicate
from .is_fixed import is_fixed


class is_with(Predicate):
    """
    A predicate that can set context that can then be retrieved using Get
    objects.
    """

    fail = is_fixed(False, 'set_failed', 'Failed to set context.')

    def __init__(self, key, transform, success, fail=fail):
        self._key = key
        self._transform = transform
        self._success = success
        self._fail = fail

    def _evaluate(self, data, explain, context):
        try:
            context.push(self._key, self._transform(data))
        except Exception:
            return self._fail(data, explain, context)
        else:
            res = self._success(data, explain, context)
            context.pop(self._key)
            return res
