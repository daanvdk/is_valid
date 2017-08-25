from .type_predicates import is_iterable, is_list, is_dict, is_tuple, is_set


def is_iterable_where(*validators):
    def is_valid(data, detailed=False):
        valid, errors = is_iterable(data, detailed=True)
        if not valid:
            return (valid, errors) if detailed else valid
        if len(data) != len(validators):
            return (
                False, {'*': 'data has incorrect length'}
            ) if detailed else False
        if not detailed:
            return all(
                validator(value) for validator, value in zip(validators, data)
            )
        errors = {}
        for i, (validator, value) in enumerate(zip(validators, data)):
            valid, suberrors = validator(value, detailed=True)
            if not valid:
                errors[i] = suberrors
        return (False, errors) if errors else (True, None)
    return is_valid


def is_iterable_of(validator):
    def is_valid(data, detailed=False):
        valid, errors = is_iterable(data, detailed=True)
        if not valid:
            return (valid, errors) if detailed else valid
        if not detailed:
            return all(validator(value) for value in data)
        errors = {}
        for i, value in enumerate(data):
            valid, suberrors = validator(value, detailed=True)
            if not valid:
                errors[i] = suberrors
        return (False, errors) if errors else (True, None)
    return is_valid


def is_dict_where(**validators):
    def is_valid(data, detailed=False):
        valid, errors = is_dict(data, detailed=True)
        if not valid:
            return (False, errors) if detailed else False
        if set(data) != set(validators):
            return (
                False, 'the data keys are not equal to the validator keys'
            ) if detailed else False
        if not detailed:
            return all(validators[key](value) for key, value in data.items())
        errors = {}
        for key, value in data.items():
            valid, suberrors = validators[key](value, detailed=True)
            if not valid:
                errors[key] = suberrors
        return (False, errors) if errors else (True, None)
    return is_valid


def is_subdict_where(**validators):
    def is_valid(data, detailed=False):
        valid, errors = is_dict(data, detailed=True)
        if not valid:
            return (False, errors) if detailed else False
        if not set(data) <= set(validators):
            return (
                False, 'the data keys are not a subset of the validator keys'
            ) if detailed else False
        if not detailed:
            return all(validators[key](value) for key, value in data.items())
        errors = {}
        for key, value in data.items():
            valid, suberrors = validators[key](value, detailed=True)
            if not valid:
                errors[key] = suberrors
        return (False, errors) if errors else (True, None)
    return is_valid


def is_superdict_where(**validators):
    def is_valid(data, detailed=False):
        valid, errors = is_dict(data, detailed=True)
        if not valid:
            return (False, errors) if detailed else False
        if not set(data) >= set(validators):
            return (
                False, 'the data keys are not a superset of the validator keys'
            ) if detailed else False
        if not detailed:
            return all(
                validator(data[key]) for key, validator in validators.items()
            )
        errors = {}
        for key, validator in validators.items():
            valid, suberrors = validator(data[key], detailed=True)
            if not valid:
                errors[key] = suberrors
        return (False, errors) if errors else (True, None)
    return is_valid


def is_object_where(**validators):
    def is_valid(data, detailed=False):
        errors = {}
        for attr, validator in validators.items():
            if hasattr(data, attr):
                valid, error = validator(getattr(data, attr), detailed=True)
                if not valid:
                    if not detailed:
                        return False
                    errors[attr] = error
            else:
                if not detailed:
                    return False
                errors[attr] = 'data does not have this attribute'
        if not detailed:
            return True
        return (False, errors) if errors else (True, None)
    return is_valid


def is_list_where(*validators):
    validator = is_iterable_where(*validators)

    def is_valid(data, detailed=False):
        valid, errors = is_list(data, detailed=True)
        if not valid:
            return (False, errors) if detailed else False
        return validator(data, detailed=detailed)
    return is_valid


def is_list_of(validator):
    validator = is_iterable_of(validator)

    def is_valid(data, detailed=False):
        valid, errors = is_list(data, detailed=True)
        if not valid:
            return (False, errors) if detailed else False
        return validator(data, detailed=detailed)
    return is_valid


def is_tuple_where(*validators):
    validator = is_iterable_where(*validators)

    def is_valid(data, detailed=False):
        valid, errors = is_tuple(data, detailed=True)
        if not valid:
            return (False, errors) if detailed else False
        return validator(data, detailed=detailed)
    return is_valid


def is_tuple_of(validator):
    validator = is_iterable_of(validator)

    def is_valid(data, detailed=False):
        valid, errors = is_tuple(data, detailed=True)
        if not valid:
            return (False, errors) if detailed else False
        return validator(data, detailed=detailed)
    return is_valid


def is_set_of(validator):
    validator = is_iterable_of(validator)

    def is_valid(data, detailed=False):
        valid, errors = is_set(data, detailed=True)
        if not valid:
            return (False, errors) if detailed else False
        if not detailed:
            return validator(data)
        elems = list(data)
        valid, errors = validator(elems, detailed=True)
        if not valid:
            return (False, {
                elems[key]: value for key, value in errors.items()
            })
        return (True, None)
    return is_valid
