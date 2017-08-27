from .type_predicates import is_iterable, is_list, is_dict, is_tuple, is_set
from .condition_predicates import is_if


def is_iterable_where(*predicates):
    """
    Generates a predicate that checks that the data is an iterable where
    the 1st element of the data is valid according to the 1st given predicate,
    the 2nd element of the data is valid according to the 2nd given predicate
    and so on. Also requires that the amount of elements in the iterable is
    equal to the amount of predicates given.
    """
    def is_valid(data, explain=False):
        if len(data) != len(predicates):
            return (
                False, 'data has incorrect length'
            ) if explain else False
        if not explain:
            return all(
                predicate(value) for predicate, value in zip(predicates, data)
            )
        reasons, errors = {}, {}
        for i, (predicate, value) in enumerate(zip(predicates, data)):
            valid, explanation = predicate(value, explain=True)
            (reasons if valid else errors)[i] = explanation
        return (True, reasons) if not errors else (False, errors)
    return is_if(is_iterable, is_valid, else_valid=False)


def is_iterable_of(predicate):
    """
    Generates a predicate that checks that the data is an iterable where
    every element of the data is valid according to the given predicate.
    """
    def is_valid(data, explain=False):
        if not explain:
            return all(predicate(value) for value in data)
        reasons, errors = {}, {}
        for i, value in enumerate(data):
            valid, explanation = predicate(value, explain=True)
            (reasons if valid else errors)[i] = explanation
        return (True, reasons) if not errors else (False, errors)
    return is_if(is_iterable, is_valid, else_valid=False)


def is_dict_where(*args, **kwargs):
    """
    Generates a predicate that checks that the data is a dict where for every
    key the value corresponding to that key is valid according to the given
    predicate corresponding to that key. If the keys of the data and the keys
    of the given predicates do not match the data is considered invalid.

    The arguments for this function work exactly the same as that of the dict
    constructor.
    """
    predicates = dict(*args, **kwargs)

    def is_valid(data, explain=False):
        if set(data) != set(predicates):
            return (
                False, 'the data keys are not equal to the predicate keys'
            ) if explain else False
        if not explain:
            return all(predicates[key](value) for key, value in data.items())
        reasons, errors = {}, {}
        for key, value in data.items():
            valid, explanation = predicates[key](value, explain=True)
            (reasons if valid else errors)[key] = explanation
        return (True, reasons) if not errors else (False, errors)
    return is_if(is_dict, is_valid, else_valid=False)


def is_subdict_where(*args, **kwargs):
    """
    Generates a predicate that checks that the data is a dict where for every
    key the value corresponding to that key is valid according to the given
    predicate corresponding to that key. If not all of the keys in the data
    have a corresponding predicate the data is considered invalid.

    The arguments for this function work exactly the same as that of the dict
    constructor.
    """
    predicates = dict(*args, **kwargs)

    def is_valid(data, explain=False):
        if not set(data) <= set(predicates):
            return (
                False, 'the data keys are not a subset of the predicate keys'
            ) if explain else False
        if not explain:
            return all(predicates[key](value) for key, value in data.items())
        reasons, errors = {}, {}
        for key, value in data.items():
            valid, explanation = predicates[key](value, explain=True)
            (reasons if valid else errors)[key] = explanation
        return (True, reasons) if not errors else (False, errors)
    return is_if(is_dict, is_valid, else_valid=False)


def is_superdict_where(*args, **kwargs):
    """
    Generates a predicate that checks that the data is a dict where for every
    key the value corresponding to that key is valid according to the given
    predicate corresponding to that key. If not all of the keys in the given
    predicates are in the data the data is considered invalid.

    The arguments for this function work exactly the same as that of the dict
    constructor.
    """
    predicates = dict(*args, **kwargs)

    def is_valid(data, explain=False):
        if not set(data) >= set(predicates):
            return (
                False, 'the data keys are not a superset of the predicate keys'
            ) if explain else False
        if not explain:
            return all(
                predicate(data[key]) for key, predicate in predicates.items()
            )
        reasons, errors = {}, {}
        for key, predicate in predicates.items():
            valid, explanation = predicate(data[key], explain=True)
            (reasons if valid else errors)[key] = explanation
        return (True, reasons) if not errors else (False, errors)
    return is_if(is_dict, is_valid, else_valid=False)


def is_dict_of(key_predicate, val_predicate):
    """
    Generates a predicate that checks that the data is a dict where every key
    is valid according to ``key_predicate`` and every value is valid according
    to ``val_predicate``.
    """
    def is_valid(data, explain=False):
        if not explain:
            return all(
                key_predicate(key) and val_predicate(val)
                for key, val in data.items()
            )
        reasons, errors = {}, {}
        for key, val in data.items():
            reason, error = {}, {}
            key_valid, key_explanation = key_predicate(key, explain=True)
            (reason if key_valid else error)['key'] = key_explanation
            val_valid, val_explanation = val_predicate(val, explain=True)
            (reason if val_valid else error)['value'] = val_explanation
            if not error:
                reasons[key] = reason
            else:
                errors[key] = error
        return (True, reasons) if not errors else (False, errors)
    return is_if(is_dict, is_valid, else_valid=False)


def is_object_where(**predicates):
    """
    Generates a predicate that checks that the data is an object where every
    given predicate holds for the associated attribute on the object.
    """
    def is_valid(data, explain=False):
        reasons, errors = {}, {}
        for attr, predicate in predicates.items():
            if hasattr(data, attr):
                valid, explanation = predicate(
                    getattr(data, attr), explain=True
                )
                if not valid and not explain:
                    return False
                (reasons if valid else errors)[attr] = explanation
            else:
                if not explain:
                    return False
                errors[attr] = 'data does not have this attribute'
        if not explain:
            return True
        return (True, reasons) if not errors else (False, errors)
    return is_valid


def is_list_where(*predicates):
    """
    Generates a predicate that checks that the data is a list where the 1st
    element of the data is valid according to the 1st given predicate, the 2nd
    element of the data is valid according to the 2nd given predicate and so
    on. Also requires that the amount of elements in the list is equal to the
    amount of predicates given.
    """
    return is_if(is_list, is_iterable_where(*predicates), else_valid=False)


def is_list_of(predicate):
    """
    Generates a predicate that checks that the data is a list where every
    element of the data is valid according to the given predicate.
    """
    return is_if(is_list, is_iterable_of(predicate), else_valid=False)


def is_tuple_where(*predicates):
    """
    Generates a predicate that checks that the data is a tuple where the 1st
    element of the data is valid according to the 1st given predicate, the 2nd
    element of the data is valid according to the 2nd given predicate and so
    on. Also requires that the amount of elements in the tuple is equal to the
    amount of predicates given.
    """
    return is_if(is_tuple, is_iterable_where(*predicates), else_valid=False)


def is_tuple_of(predicate):
    """
    Generates a predicate that checks that the data is a tuple where every
    element of the data is valid according to the given predicate.
    """
    return is_if(is_tuple, is_iterable_of(predicate), else_valid=False)


def is_set_of(predicate):
    """
    Generates a predicate that checks that the data is a set where every
    element of the data is valid according to the given predicate.
    """
    predicate = is_iterable_of(predicate)

    def is_valid(data, explain=False):
        if not explain:
            return predicate(data)
        elems = list(data)
        valid, explanation = predicate(elems, explain=True)
        return (True, explanation) if valid else (False, {
            elems[i]: value for i, value in explanation.items()
        })
    return is_if(is_set, is_valid, else_valid=False)
