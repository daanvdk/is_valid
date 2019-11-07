from collections import defaultdict

from .explanation import Explanation
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

    def __call__(self, data, explain=False, context={}):
        if not isinstance(context, Context):
            context = Context(context)

        try:
            for prerequisite in self.prerequisites:
                res = prerequisite(data, explain, context)
                if explain:
                    data = res.data
                if not res:
                    break
            else:
                res = self._evaluate(data, explain, context)
        except ContextError as e:
            res = e.explanation if explain else False

        if explain and not hasattr(res, 'data'):
            res = res.copy(data=data)
        return res

    def explain(self, data, context={}):
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


class ContextError(Exception):
    def __init__(self, key):
        self.explanation = Explanation(
            False, 'context_missing',
            'No context found for key \'{}\''.format(key),
        )
        super().__init__(self.explanation.message)


class Context(object):

    def __init__(self, base={}):
        self._values = defaultdict(list)
        for key, value in base.items():
            self.push(key, value)

    def push(self, key, value):
        self._values[key].append(value)

    def pop(self, key):
        self._values[key].pop()
        if not self._values[key]:
            del self._values[key]

    def __call__(self, value):
        if isinstance(value, Get):
            if not self._values[value._key]:
                raise ContextError(value._key)
            return value._transform(self._values[value._key][-1])
        return value


def instantiate(func):
    return func()
