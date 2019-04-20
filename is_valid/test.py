from .to_pred import to_pred


def assert_valid(data, predicate, context={}, message=None):
    """
    Asserts that the data is valid according to the given predicate. If no
    ``message`` is provided to this function the explanation of the predicate
    will be used for the AssertionError in case the assertion fails.
    """
    valid = to_pred(predicate).explain(data, context=context)

    if not valid:
        if message is None:
            message = valid.summary()
        raise AssertionError(message)

    return valid.data
