from .is_eq import to_pred


class assert_valid(object):
    """
    Creates a function that asserts that the data is valid according to the
    given predicate. If no ``message`` is provided to this function the
    explanation of the predicate will be used for the AssertionError in case
    the assertion fails.
    """

    def __init__(self, predicate):
        self._predicate = to_pred(predicate)

    def __call__(self, data, message=None, advanced=True):
        if message is None:
            explanation = self._predicate.explain(data)
            valid = explanation.valid
            message = (repr if advanced else str)(explanation)
        else:
            valid = self._predicate(data)
        if not valid:
            raise AssertionError(message)
