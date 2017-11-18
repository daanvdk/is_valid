from .expression_predicates import is_eq


def assert_valid(predicate):
    """
    Creates a function that asserts that the data is valid according to the
    given predicate. If no ``msg`` is provided to this function the explanation
    of the predicate will be used for the AssertionError in case the assertion
    fails.
    """
    if not callable(predicate):
        predicate = is_eq(predicate)

    def res(data, msg=None):
        if msg is None:
            valid, explanation = predicate(data, explain=True)
        else:
            valid, explanation = predicate(data), msg
        if not valid:
            raise AssertionError(str(explanation))
    return res
