from .explanation import Explanation
from .base_predicates import is_fixed
from .expression_predicates import is_eq


def is_any(*predicates):
    """
    Generates a predicate that will consider data valid if and only if any of
    the given predicates considers the data valid.
    """
    predicates = [
        predicate if callable(predicate) else is_eq(predicate)
        for predicate in predicates
    ]

    def is_valid(data, explain=False):
        if not explain:
            return any(predicate(data) for predicate in predicates)
        reasons, errors = [], []
        for i, predicate in enumerate(predicates):
            explanation = predicate(data, explain=True)
            (reasons if explanation else errors).append(explanation)
        return Explanation(
            True, 'any_holds',
            'At least one of the given predicates holds.',
            reasons,
        ) if reasons else Explanation(
            False, 'not_any_holds',
            'None of the given predicates holds.',
            errors,
        )
    return is_valid


def is_all(*predicates):
    """
    Generates a predicate that will consider data valid if and only if all of
    the given predicates considers the data valid.
    """
    predicates = [
        predicate if callable(predicate) else is_eq(predicate)
        for predicate in predicates
    ]

    def is_valid(data, explain=False):
        if not explain:
            return all(predicate(data) for predicate in predicates)
        reasons, errors = [], []
        for i, predicate in enumerate(predicates):
            explanation = predicate(data, explain=True)
            (reasons if explanation else errors).append(explanation)
        return Explanation(
            True, 'all_hold',
            'All of the given predicates hold.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_all_hold',
            'At least one of the given predicates does not hold.',
            errors,
        )
    return is_valid


def is_one(*predicates):
    """
    Generates a predicate that will consider data valid if and only if exactly
    one of the given predicates considers the data valid.
    """
    predicates = [
        predicate if callable(predicate) else is_eq(predicate)
        for predicate in predicates
    ]

    def is_valid(data, explain=False):
        if not explain:
            one = False
            for predicate in predicates:
                if predicate(data):
                    if one:
                        return False
                    one = True
            return one
        reasons, errors = [], []
        for i, predicate in enumerate(predicates):
            explanation = predicate(data, explain=True)
            (reasons if explanation else errors).append(explanation)
        return Explanation(
            True, 'one_holds',
            'Exactly one of the given predicates hold.',
            reasons[0],
         ) if len(reasons) == 1 else Explanation(
            False, 'none_hold',
            'None of the given predicates hold.',
            errors,
         ) if len(reasons) == 0 else Explanation(
             False, 'multiple_hold',
            'Multiple of the given predicates hold.',
            reasons,
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
    if not callable(condition):
        condition = is_eq(condition)
    if not callable(if_predicate):
        if_predicate = is_eq(if_predicate)
    if else_predicate is not None and not callable(else_predicate):
        else_predicate = is_eq(else_predicate)

    if else_predicate:
        return lambda data, explain=False: (
            if_predicate if condition(data) else else_predicate
        )(data, explain=explain)
    else:
        def is_valid(data, explain=False):
            if not explain:
                return if_predicate(data) if condition(data) else else_valid
            explanation = condition(data, explain=True)
            if explanation:
                return if_predicate(data, explain=True)
            explanation.valid = else_valid
            return explanation
        return is_valid


def is_cond(
    *conditions,
    default=is_fixed(False, 'no_match', 'None of the conditions match.')
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
    is_valid = default if callable(default) else is_eq(default)
    for condition, predicate in reversed(conditions):
        is_valid = is_if(condition, predicate, is_valid)
    return is_valid
