from .to_pred import to_pred


def assert_valid(data, predicate, context={}, message=None, advanced=True):
    """
    Asserts that the data is valid according to the given predicate. If no
    ``message`` is provided to this function the explanation of the predicate
    will be used for the AssertionError in case the assertion fails.
    """
    predicate = to_pred(predicate)

    if message is None:
        explanation = predicate.explain(data, context=context)
        valid = explanation.valid
        message = (repr if advanced else str)(explanation)
    else:
        valid = predicate(data)

    if not valid:
        raise AssertionError(message)
