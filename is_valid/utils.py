from .explanation import Explanation


def explain(
    predicate,
    code='valid',
    message_valid='data is valid',
    message_invalid='data is not valid',
    details_valid=None,
    details_invalid=None,
):
    """
    Wraps a predicate with an explanation. You can set the explanation messages
    with the parameters ``explanation_valid`` and ``explanation_invalid``.

    This method is also very nice way to use predicates from other sources than
    `Is Valid?` that don't have an ``explain`` parameter to work with
    explanations.
    """
    return lambda data, explain=False: (
        Explanation(True, code, message_valid, details_valid)
        if predicate(data) else
        Explanation(False, 'not_' + code, message_invalid, details_invalid)
    ) if explain else predicate(data)
