

def explain(
    predicate,
    explanation_valid='data is valid',
    explanation_invalid='data is not valid'
):
    """
    Wraps a predicate with an explanation. You can set the explanation messages
    with the parameters ``explanation_valid`` and ``explanation_invalid``.

    This method is also very nice way to use predicates from other sources than
    `Is Valid?` that don't have an ``explain`` parameter to work with
    explanations.
    """
    return lambda data, explain=False: (
        (True, explanation_valid)
        if predicate(data) else
        (False, explanation_invalid)
    ) if explain else predicate(data)
