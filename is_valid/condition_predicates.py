from .base_predicates import is_fixed


def is_any(*predicates):
    """
    Generates a predicate that will consider data valid if and only if any of
    the given predicates considers the data valid.
    """
    def is_valid(data, explain=False):
        if not explain:
            return any(predicate(data) for predicate in predicates)
        reasons, errors = [], []
        for i, predicate in enumerate(predicates):
            valid, explanation = predicate(data, explain=True)
            (reasons if valid else errors).append(explanation)
        return (True, reasons) if reasons else (False, errors)
    return is_valid


def is_all(*predicates):
    """
    Generates a predicate that will consider data valid if and only if all of
    the given predicates considers the data valid.
    """
    def is_valid(data, explain=False):
        if not explain:
            return all(predicate(data) for predicate in predicates)
        reasons, errors = [], []
        for i, predicate in enumerate(predicates):
            valid, explanation = predicate(data, explain=True)
            (reasons if valid else errors).append(explanation)
        return (True, reasons) if not errors else (False, errors)
    return is_valid


def is_one(*predicates):
    """
    Generates a predicate that will consider data valid if and only if exactly
    one of the given predicates considers the data valid.
    """
    def is_valid(data, explain=False):
        if not explain:
            return sum(1 for p in predicates if p(data)) == 1
        explanation = {True: [], False: []}
        for i, predicate in enumerate(predicates):
            valid, subexplanation = predicate(data, explain=True)
            explanation[valid].append(subexplanation)
        return (
            True, explanation
        ) if len(explanation[True]) == 1 else (
            False, explanation
        )
    return is_valid


def is_if(condition, if_predicate, else_predicate=None, else_valid=True):
    """
    Generates a predicate that given a predicate as condition will based on the
    result of this condition on the data evaluate the data with either
    ``if_predicate`` or ``else_predicate``. If else predicate is omitted it
    will use the value of ``else_valid`` for when the condition considers the
    data invalid, as explanation it will reuse the explanation that the
    condition returned.
    """
    def is_valid(data, explain=False):
        if else_predicate:
            return (
                if_predicate if condition(data) else else_predicate
            )(data, explain=explain)
        if not explain:
            return if_predicate(data) if condition(data) else else_valid
        valid, explanation = condition(data, explain=True)
        return if_predicate(data, explain=True) if valid else (
            else_valid, explanation
        )
    return is_valid


def is_cond(
    *conditions,
    default=is_fixed(False, 'data matches none of the conditions')
):
    """
    Generates a predicate that given pairs of condition and validation
    predicates (represented as 2-tuples) returns the result of the validation
    predicate that corresponds to the first condition predicate that holds
    for the given data. If none of the condition predicates hold the predicate
    with the ``default`` keyword argument will be used. By default this will
    always consider the data invalid with the explanation that the data matches
    none of the conditions.
    """
    is_valid = default
    for condition, predicate in reversed(conditions):
        is_valid = is_if(condition, predicate, is_valid)
    return is_valid
