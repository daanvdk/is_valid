import json

from .condition_predicates import is_if
from .type_predicates import is_str


def is_transformed(
    transform, predicate, *args,
    exceptions=[Exception], msg='data can\'t be transformed', **kwargs
):
    """
    Generates a predicate that checks if the data is valid according to some
    predicate after a function has been applied to the data. If this function
    throws an exception the predicate will consider the data invalid.

    With the ``exceptions`` parameter you can limit the exceptions that the
    predicate catches. With the ``msg`` parameter you can specify what the
    explanation should be when the predicate catches an exception.

    The predicate that this function returns also has an optional ``include``
    parameter, if you set this to ``True`` the data after the transformation
    will also be returned in case the transformation was succesful.

    All other arguments provided will be passed on to the transform function.
    """
    def is_valid(data, explain=False):
        try:
            data = transform(data, *args, **kwargs)
        except Exception as e:
            if not any(isinstance(e, exc) for exc in exceptions):
                raise e
            return (False, msg) if explain else False
        return predicate(data, explain=explain)
    return is_valid


def is_json_where(predicate, *args, loader=json.loads, **kwargs):
    """
    Generates a predicate that checks if the data is valid according to some
    predicate after it has been decoded as JSON. The predicate considers the
    data invalid if it is invalid JSON.

    With the ``loader`` parameter you can specify a different loader than the
    default JSON loader.

    All other arguments provided will be passed on to the JSON loader.
    """
    return is_if(is_str, is_transformed(
        loader, predicate, *args,
        exceptions=[ValueError], msg='data is not valid json', **kwargs
    ), else_valid=False)
