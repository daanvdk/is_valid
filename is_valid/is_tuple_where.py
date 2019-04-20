from .is_iterable_where import is_iterable_where
from .is_tuple import is_tuple


class is_tuple_where(is_iterable_where):
    """
    Generates a predicate that checks that the data is a tuple where the 1st
    element of the data is valid according to the 1st given predicate, the 2nd
    element of the data is valid according to the 2nd given predicate and so
    on. Also requires that the amount of elements in the tuple is equal to the
    amount of predicates given.
    """

    prerequisites = [is_tuple]

    def _evaluate(self, data, explain, context):
        res = super()._evaluate(data, explain, context)
        if explain:
            res.data = tuple(res.data)
        return res
