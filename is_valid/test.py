from .expression_predicates import is_eq


def assert_valid(predicate):
    """
    Creates a function that asserts that the data is valid according to the
    given predicate. If no ``message`` is provided to this function the
    explanation of the predicate will be used for the AssertionError in case
    the assertion fails.
    """
    if not callable(predicate):
        predicate = is_eq(predicate)

    def res(data, message=None, advanced=True):
        if message is None:
            explanation = predicate(data, explain=True)
            valid = explanation.valid
            message = (repr if advanced else str)(explanation)
        else:
            valid = predicate(data)
        if not valid:
            raise AssertionError(message)
    return res
