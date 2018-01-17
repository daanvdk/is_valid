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
        self._context = isinstance(predicate, Predicate)
        self._predicate = predicate
        self._valid_exp = Explanation(
            True, code, message_valid, details_valid
        )
        self._not_valid_exp = Explanation(
            False, 'not_{}'.format(code), message_invalid, details_invalid
        )

    def _evaluate(self, data, explain, context):
        return (
            (self._valid_exp if explain else True) if (
                self._predicate(data, context=context)
                if self._context else
                self._predicate(data)
            ) else (self._not_valid_exp if explain else False)
        )


class Wrapper:

    def __init__(self, wrapped=None):
        super().__setattr__('_wrapped', wrapped)

    def wrap(self, wrapped):
        super().__setattr__('_wrapped', wrapped)

    def __getattr__(self, attr):
        return getattr(self._wrapped, attr)

    def __setattr__(self, attr, value):
        setattr(self._wrapped, attr, value)

    def __call__(self, *args, **kwargs):
        if self._wrapped is None:
            raise AttributeError('Wrapper has nothing wrapped.')
        return self._wrapped(*args, **kwargs)
