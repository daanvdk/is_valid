import json
from datetime import datetime, date, time, timedelta

from .utils import explain


def _is_iterable(data):
    try:
        iter(data)
        return True
    except TypeError:
        return False


#: A predicate that checks if the data is iterable.
is_iterable = explain(
    _is_iterable, 'iterable', 'Data is iterable.', 'Data is not iterable.'
)


def is_instance(cls, rep=None):
    """
    Generates a predicate that checks if the data is an instance of the given
    class. You can use the ``rep`` argument to specify what an instance of this
    class should be called. If you don't do this it will default to ``an
    instance of {cls.__name__}``.
    """
    if rep is None:
        rep = 'an instance of {}'.format(cls.__name__)
    return explain(
        lambda data: isinstance(data, cls),
        'instance_of', 'Data is {}'.format(rep), 'Data is not {}'.format(rep),
    )


#: A predicate that checks if the data is a string.
is_str = is_instance(str, rep='a str')
#: A predicate that checks if the data is an integer.
is_int = is_instance(int, rep='an int')
#: A predicate that checks if the data is a float.
is_float = is_instance(float, rep='a float')
#: A predicate that checks if the data is a boolean.
is_bool = is_instance(bool, rep='a bool')
#: A predicate that checks if the data is a list.
is_list = is_instance(list, rep='a list')
#: A predicate that checks if the data is a dictionary.
is_dict = is_instance(dict, rep='a dict')
#: A predicate that checks if the data is a set.
is_set = is_instance(set, rep='a set')
#: A predicate that checks if the data is a tuple.
is_tuple = is_instance(tuple, rep='a tuple')
#: A predicate that checks if the data is a datetime.
is_datetime = is_instance(datetime, rep='a datetime')
#: A predicate that checks if the data is a date.
is_date = is_instance(date, rep='a date')
#: A predicate that checks if the data is a time.
is_time = is_instance(time, rep='a time')
#: A predicate that checks if the data is a timedelta.
is_timedelta = is_instance(timedelta, rep='a timedelta')
#: A predicate that checks if the data is a number.
is_number = is_instance((int, float), rep='a number')


def _is_json(data):
    try:
        json.loads(data)
        return True
    except ValueError:
        return False


#: A predicate that checks if the data is valid json.
is_json = explain(
    _is_json, 'json', 'Data is valid json.', 'Data is not valid json.'
)
