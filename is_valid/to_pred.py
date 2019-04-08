from .base import Predicate


def to_pred(value):
    if isinstance(value, Predicate):
        return value
    elif isinstance(value, dict):
        from .is_dict_where import is_dict_where
        return is_dict_where(value)
    elif isinstance(value, list):
        from .is_list_where import is_list_where
        return is_list_where(*value)
    elif isinstance(value, tuple):
        from .is_tuple_where import is_tuple_where
        return is_tuple_where(*value)
    else:
        from .is_eq import is_eq
        return is_eq(value)
