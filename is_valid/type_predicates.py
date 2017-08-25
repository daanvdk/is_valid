from datetime import datetime, date, time, timedelta


def is_iterable(data, explain=False):
    try:
        iter(data)
        return (True, 'data is iterable') if explain else True
    except TypeError:
        return (False, 'data is not iterable') if explain else False


def is_instance(cls, rep=None):
    if rep is None:
        rep = 'an instance of {}'.format(cls.__name__)

    def is_valid(data, explain=False):
        if not explain:
            return isinstance(data, cls)
        return (
            True, 'data is {}'.format(rep)
        ) if isinstance(data, cls) else (
            False, 'data is not {}'.format(rep)
        )
    return is_valid


is_str = is_instance(str, rep='a str')
is_int = is_instance(int, rep='an int')
is_float = is_instance(float, rep='a float')
is_bool = is_instance(bool, rep='a bool')
is_list = is_instance(list, rep='a list')
is_dict = is_instance(dict, rep='a dict')
is_set = is_instance(set, rep='a set')
is_tuple = is_instance(tuple, rep='a tuple')
is_datetime = is_instance(datetime, rep='a datetime')
is_date = is_instance(date, rep='a date')
is_time = is_instance(time, rep='a time')
is_timedelta = is_instance(timedelta, rep='a timedelta')
is_number = is_instance((int, float), rep='a number')
