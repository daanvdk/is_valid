from .base import Predicate
from .explanation import Explanation
from .to_pred import to_pred


class is_pre(Predicate):
    """
    Given some predicates this creates a predicate that will try to see if all
    the given predicates hold. This differs from `is_all` in that this
    predicate will stop evaluation after the first failure and will only return
    the result of the last predicate on success. This makes it very suitable
    for adding preconditions where you only want to use later predicates
    when you know the previous predicates hold.

    When no predicates are given the returned predicate will be equivalent to
    `is_something`.
    """

    _base_exp = Explanation(True, 'is_something', 'data is something')

    def __init__(self, *predicates):
        self._predicates = [to_pred(predicate) for predicate in predicates]

    def _evaluate(self, data, explain, context):
        valid = self._base_exp if explain else True
        for predicate in self._predicates:
            if not valid:
                break
            valid = predicate(data, explain, context)
            if explain:
                data = valid.data
        return valid
