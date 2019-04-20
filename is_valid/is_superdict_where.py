from .is_dict_where import is_dict_where
from .is_something import is_something


class is_superdict_where(is_dict_where):
    """
    Generates a predicate that checks that the data is a dict where for every
    key the value corresponding to that key is valid according to the given
    predicate corresponding to that key. If not all of the keys in the given
    predicates are in the data the data is considered invalid.

    The arguments for this function work exactly the same as that of the dict
    constructor.
    """

    _extra_pred = is_something
