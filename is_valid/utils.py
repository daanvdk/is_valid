from .base import Predicate
from .explanation import Explanation
from .is_eq import is_eq


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
        self._predicate = predicate
        self._valid_exp = Explanation(
            True, code, message_valid, details_valid
        )
        self._not_valid_exp = Explanation(
            False, 'not_{}'.format(code), message_invalid, details_invalid
        )

    def _evaluate(self, data, explain):
        return (
            (self._valid_exp if explain else True)
            if self._predicate(data) else
            (self._not_valid_exp if explain else False)
        )


class Wrapper:

    def __init__(self, func=None):
        self.func = func

    def __call__(self, *args, **kwargs):
        if self.func is None:
            raise AttributeError('Wrapper has no function.')
        return self.func(*args, **kwargs)
