from collections import defaultdict
from .get import Get


class Predicate(object):

    prerequisites = []

    def _evaluate(self, data, explain, context):
        return (
            self._evaluate_explain
            if explain else
            self._evaluate_no_explain
        )(data, context)

    def _evaluate_explain(self, data, context):
        raise NotImplementedError('evaluate_explain is not implemented.')

    def _evaluate_no_explain(self, data, context):
        raise NotImplementedError('evaluate_no_explain is not implemented.')

    def __call__(self, data, explain=False, context=None):
        if context is None:
            context = Context()
        for prerequisite in self.prerequisites:
            res = prerequisite(data, explain, context)
            if not res:
                return res
        return self._evaluate(data, explain, context)

    def explain(self, data, context=None):
        return self(data, True, context)

    def __and__(self, other):
        from .is_all import is_all
        return is_all(self, other)

    def __or__(self, other):
        from .is_any import is_any
        return is_any(self, other)

    def __invert__(self):
        from .is_not import is_not
        return is_not(self)


class Context(object):

    def __init__(self):
        self._values = defaultdict(list)

    def push(self, key, value):
        self._values[key].append(value)

    def pop(self, key):
        self._values[key].pop()

    def __call__(self, value):
        if isinstance(value, Get):
            if not self._values[value._key]:
                raise ValueError(
                    'Context has no value for key: {}'.format(value._key)
                )
            return value._transform(self._values[value._key][-1])
        return value


def instantiate(func):
    return func()
