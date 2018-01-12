from .is_iterable_where import is_iterable_where
from .is_list import is_list


class is_list_where(is_iterable_where):
    """
    Generates a predicate that checks that the data is a list where the 1st
    element of the data is valid according to the 1st given predicate, the 2nd
    element of the data is valid according to the 2nd given predicate and so
    on. Also requires that the amount of elements in the list is equal to the
    amount of predicates given.
    """

    prerequisites = [is_list]
