from datetime import datetime, date, time, timedelta
import re


def is_iterable(data, detailed=False):
    try:
        iter(data)
        return (True, None) if detailed else True
    except TypeError:
        return (False, 'data is not iterable') if detailed else False


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


def is_instance(cls, rep=None):
    if rep is None:
        rep = cls.__name__

    def is_valid(data, detailed=False):
        if not detailed:
            return isinstance(data, cls)
        return (
            False, 'data is not an instance of {}'.format(rep)
        ) if not isinstance(data, cls) else (True, None)
    return is_valid


def is_eq(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, detailed=False):
        if not detailed:
            return data == value
        return (
            False, 'data is not equal to {}'.format(rep)
        ) if not data == value else (True, None)
    return is_valid


def is_neq(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, detailed=False):
        if not detailed:
            return data != value
        return (
            False, 'data is not not equal to {}'.format(rep)
        ) if not data != value else (True, None)
    return is_valid


def is_gt(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, detailed=False):
        if not detailed:
            return data > value
        return (
            False, 'data is not greater than {}'.format(rep)
        ) if not data > value else (True, None)
    return is_valid


def is_geq(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, detailed=False):
        if not detailed:
            return data >= value
        return (
            False, 'data is not greater than or equal to {}'.format(rep)
        ) if not data >= value else (True, None)
    return is_valid


def is_lt(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, detailed=False):
        if not detailed:
            return data < value
        return (
            False, 'data is not lower than {}'.format(rep)
        ) if not data < value else (True, None)
    return is_valid


def is_leq(value, rep=None):
    if rep is None:
        rep = repr(value)

    def is_valid(data, detailed=False):
        if not detailed:
            return data <= value
        return (
            False, 'data is not lower than or equal to {}'.format(rep)
        ) if not data <= value else (True, None)
    return is_valid


def is_in(collection):
    def is_valid(data, detailed=False):
        if not detailed:
            return data in collection
        return (
            False, 'data is not in collection'
        ) if data not in collection else (True, None)
    return is_valid


def is_not_in(collection):
    def is_valid(data, detailed=False):
        if not detailed:
            return data not in collection
        return (
            False, 'data is not not in collection'
        ) if data in collection else (True, None)
    return is_valid


def is_anything(data, detailed=False):
    return (True, None) if detailed else True


def is_none(data, detailed=False):
    if not detailed:
        return data is None
    return (False, 'data is not None') if data is not None else (True, None)


def is_not_none(data, detailed=False):
    if not detailed:
        return data is None
    return (False, 'data is not not None') if data is None else (True, None)


def is_not(validator):
    def is_valid(data, detailed=False):
        if not detailed:
            return not validator(data)
        return (
            False, 'data is not not valid according to the given validator'
        ) if validator(data) else (True, None)
    return is_valid


is_str = is_instance(str, rep='str')
is_int = is_instance(int, rep='int')
is_float = is_instance(float, rep='float')
is_bool = is_instance(bool, rep='bool')
is_list = is_instance(list, rep='list')
is_dict = is_instance(dict, rep='list')
is_set = is_instance(set, rep='list')
is_tuple = is_instance(tuple, rep='list')
is_datetime = is_instance(datetime, rep='datetime')
is_date = is_instance(date, rep='date')
is_time = is_instance(time, rep='time')
is_timedelta = is_instance(timedelta, rep='timedelta')


def is_match(regexp, flags=0):
    if isinstance(str, regexp):
        regexp = re.compile(regexp, flags=flags)
    rep = '/{}/{}'.format(regexp.pattern, ''.join(char for flag, char in [
        (re.A, 'a'), (re.I, 'i'), (re.L, 'l'),
        (re.M, 'm'), (re.S, 's'), (re.X, 'x'),
    ] if regexp.flags & flag))

    def is_valid(data, detailed=False):
        valid, errors = is_str(data, detailed=True)
        if not valid:
            return (False, errors) if detailed else False
        if regexp.match(data):
            return (True, None) if detailed else True
        return (
            False, 'data does not match {}'.format(rep)
        ) if detailed else False


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


class IsValidMixin:
    def assertIsValid(self, validator, data, msg=None):
        valid, error = validator(data, detailed=True)
        self.assertTrue(
            valid,
            msg='Error: {}'.format(error) if msg is None else msg
        )
