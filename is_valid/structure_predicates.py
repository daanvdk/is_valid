from .explanation import Explanation
from .type_predicates import is_iterable, is_list, is_dict, is_tuple, is_set
from .condition_predicates import is_if
from .expression_predicates import is_eq


def is_iterable_where(*predicates):
    """
    Generates a predicate that checks that the data is an iterable where
    the 1st element of the data is valid according to the 1st given predicate,
    the 2nd element of the data is valid according to the 2nd given predicate
    and so on. Also requires that the amount of elements in the iterable is
    equal to the amount of predicates given.
    """
    predicates = [
        predicate if callable(predicate) else is_eq(predicate)
        for predicate in predicates
    ]

    def is_valid(data, explain=False):
        data = list(data)
        if len(data) != len(predicates):
            return Explanation(
                False, 'IncorrectLength',
                'The length should be {}'.format(len(predicates)),
            ) if explain else False
        if not explain:
            return all(
                predicate(value) for predicate, value in zip(predicates, data)
            )
        reasons, errors = {}, {}
        for i, (predicate, value) in enumerate(zip(predicates, data)):
            explanation = predicate(value, explain=True)
            (reasons if explanation else errors)[i] = explanation
        return Explanation(
            True, 'all_valid',
            'All elements are valid according to their respective predicate.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_all_valid',
            'Not all elements are valid according to their respective '
            'predicate.',
            errors,
        )
    return is_if(is_iterable, is_valid, else_valid=False)


def is_iterable_of(predicate):
    """
    Generates a predicate that checks that the data is an iterable where
    every element of the data is valid according to the given predicate.
    """
    if not callable(predicate):
        predicate = is_eq(predicate)

    def is_valid(data, explain=False):
        if not explain:
            return all(predicate(value) for value in data)
        reasons, errors = {}, {}
        for i, value in enumerate(data):
            explanation = predicate(value, explain=True)
            (reasons if explanation else errors)[i] = explanation
        return Explanation(
            True, 'all_valid',
            'All elements are valid according to the predicate.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_all_valid',
            'Not all elements are valid according to the predicate.',
            errors,
        )
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
    predicates = {
        key: predicate if callable(predicate) else is_eq(predicate)
        for key, predicate in dict(*args, **kwargs).items()
    }

    def is_valid(data, explain=False):
        missing = set(predicates) - set(data)
        extra = set(data) - set(predicates)
        if missing or extra:
            return Explanation(
                False, 'keys_do_not_match',
                'The data keys are not equal to the predicate keys',
                {k: v for k, v in {
                    'missing': missing,
                    'extra': extra,
                }.items() if v},
            ) if explain else False
        if not explain:
            return all(predicates[key](value) for key, value in data.items())
        reasons, errors = {}, {}
        for key, value in data.items():
            explanation = predicates[key](value, explain=True)
            (reasons if explanation else errors)[key] = explanation
        return Explanation(
            True, 'dict_where',
            'Data is a dict where all the given predicates hold.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_dict_where',
            'Data is not a dict where all the given predicates hold.',
            errors,
        )
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
    predicates = {
        key: predicate if callable(predicate) else is_eq(predicate)
        for key, predicate in dict(*args, **kwargs).items()
    }

    def is_valid(data, explain=False):
        extra = set(data) - set(predicates)
        if extra:
            return Explanation(
                False, 'not_subdict',
                'The data keys are not a subset of the predicate keys',
                {'extra': extra},
            ) if explain else False
        if not explain:
            return all(predicates[key](value) for key, value in data.items())
        reasons, errors = {}, {}
        for key, value in data.items():
            explanation = predicates[key](value, explain=True)
            (reasons if explanation else errors)[key] = explanation
        return Explanation(
            True, 'subdict_where',
            'Data is a subdict where all the given predicates hold.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_subdict_where',
            'Data is not a subdict where all the given predicates hold.',
            errors,
        )
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
    predicates = {
        key: predicate if callable(predicate) else is_eq(predicate)
        for key, predicate in dict(*args, **kwargs).items()
    }

    def is_valid(data, explain=False):
        missing = set(predicates) - set(data)
        if missing:
            return Explanation(
                False, 'not_superdict',
                'The data keys are not a superset of the predicate keys',
                {'missing': missing},
            ) if explain else False
        if not explain:
            return all(
                predicate(data[key]) for key, predicate in predicates.items()
            )
        reasons, errors = {}, {}
        for key, predicate in predicates.items():
            explanation = predicate(data[key], explain=True)
            (reasons if explanation else errors)[key] = explanation
        return Explanation(
            True, 'superdict_where',
            'Data is a superdict where all the given predicates hold.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_superdict_where',
            'Data is not a superdict where all the given predicates hold.',
            errors,
        )
    return is_if(is_dict, is_valid, else_valid=False)


def is_dict_of(key_predicate, val_predicate):
    """
    Generates a predicate that checks that the data is a dict where every key
    is valid according to ``key_predicate`` and every value is valid according
    to ``val_predicate``.
    """
    if not callable(key_predicate):
        key_predicate = is_eq(key_predicate)
    if not callable(val_predicate):
        val_predicate = is_eq(val_predicate)

    def is_valid(data, explain=False):
        if not explain:
            return all(
                key_predicate(key) and val_predicate(val)
                for key, val in data.items()
            )
        reasons, errors = {}, {}
        for key, val in data.items():
            reason, error = {}, {}
            key_explanation = key_predicate(key, explain=True)
            (reason if key_explanation else error)['key'] = key_explanation
            val_explanation = val_predicate(val, explain=True)
            (reason if val_explanation else error)['value'] = val_explanation
            if not error:
                reasons[key] = reason
            else:
                errors[key] = error
        return Explanation(
            True, 'dict_of',
            'Data is a dict where all the entries are valid according to the '
            'given predicates.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_dict_of',
            'Data is not a dict where all the entries are valid according to '
            'the given predicates.',
            errors,
        )
    return is_if(is_dict, is_valid, else_valid=False)


def is_object_where(**predicates):
    """
    Generates a predicate that checks that the data is an object where every
    given predicate holds for the associated attribute on the object.
    """
    predicates = {
        key: predicate if callable(predicate) else is_eq(predicate)
        for key, predicate in predicates.items()
    }

    def is_valid(data, explain=False):
        reasons, errors = {}, {}
        for attr, predicate in predicates.items():
            if not explain:
                if not (
                    hasattr(data, attr) and
                    predicate(getattr(data, attr))
                ):
                    return False
            elif hasattr(data, attr):
                explanation = predicate(getattr(data, attr), explain=True)
                (reasons if explanation else errors)[attr] = explanation
            else:
                errors[attr] = Explanation(
                    False, 'no_such_attr',
                    'Data does not have this attribute.',
                )
        if not explain:
            return True
        return Explanation(
            True, 'object_where',
            'Data is an object where all the given predicates hold.',
            reasons,
        ) if not errors else Explanation(
            False, 'not_object_where',
            'Data is not an object where all the given predicates hold.',
            errors,
        )
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
        explanation = predicate(elems, explain=True)
        explanation.details = {
            elems[i]: v for i, v in explanation.details.items()
        }
        return explanation
    return is_if(is_set, is_valid, else_valid=False)
