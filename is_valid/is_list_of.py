from .is_iterable_of import is_iterable_of
from .is_list import is_list


class is_list_of(is_iterable_of):
    """
    Generates a predicate that checks that the data is a list where every
    element of the data is valid according to the given predicate.
    """

    prerequisites = [is_list]
