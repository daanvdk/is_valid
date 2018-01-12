from .is_iterable_of import is_iterable_of
from .is_tuple import is_tuple


class is_tuple_of(is_iterable_of):
    """
    Generates a predicate that checks that the data is a tuple where every
    element of the data is valid according to the given predicate.
    """

    prerequisites = [is_tuple]
