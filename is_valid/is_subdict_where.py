from .is_dict_where import is_dict_where


class is_subdict_where(is_dict_where):
    """
    Generates a predicate that checks that the data is a dict where for every
    key the value corresponding to that key is valid according to the given
    predicate corresponding to that key. If not all of the keys in the data
    have a corresponding predicate the data is considered invalid.

    The arguments for this function work exactly the same as that of the dict
    constructor.
    """

    def __init__(self, *args, **kwargs):
        super().__init__({}, dict(*args, **kwargs))
