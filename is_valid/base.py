class Predicate(object):

    prerequisites = []

    def _evaluate(self, data, explain):
        return (
            self._evaluate_explain
            if explain else
            self._evaluate_no_explain
        )(data)

    def _evaluate_explain(self, data):
        raise NotImplementedError('evaluate_explain is not implemented.')

    def _evaluate_no_explain(self, data):
        raise NotImplementedError('evaluate_no_explain is not implemented.')

    def __call__(self, data, explain=False):
        for prerequisite in self.prerequisites:
            res = prerequisite(data, explain)
            if not res:
                return res
        return self._evaluate(data, explain)

    def explain(self, data):
        return self(data, True)

    def __and__(self, other):
        from .is_all import is_all
        return is_all(self, other)

    def __or__(self, other):
        from .is_any import is_any
        return is_any(self, other)

    def __invert__(self):
        from .is_not import is_not
        return is_not(self)


def instantiate(func):
    return func()
