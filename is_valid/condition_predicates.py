from functools import reduce

from .extreme_predicates import is_anything


def is_any(*validators):
    def is_valid(data, detailed=False):
        if not detailed:
            return any(validator(data) for validator in validators)
        errors = []
        for i, validator in enumerate(validators):
            valid, suberrors = validator(data, detailed=True)
            if valid:
                return (True, None)
            errors.append(suberrors)
        return (False, errors)
    return is_valid


def is_all(*validators):
    def is_valid(data, detailed=False):
        if not detailed:
            return all(validator(data) for validator in validators)
        errors = {}
        for i, validator in enumerate(validators):
            valid, suberrors = validator(data, detailed=True)
            if not valid:
                errors[i] = suberrors
        return (False, errors) if errors else (True, None)
    return is_valid


def is_if(cond, if_validator, else_validator=is_anything):
    def is_valid(data, detailed=True):
        return (
            if_validator if cond(data) else else_validator
        )(data, detailed=detailed)


def is_cond(*conds):
    return reduce(
        lambda e, cond: is_if(cond[0], cond[1], e),
        reversed(conds),
        lambda _, detailed=False: (
            False, 'data matches none of the conditions'
        ) if detailed else False
    )
