from .base import Predicate
from .explanation import Explanation


class is_instance(Predicate):
    """
    Generates a predicate that checks if the data is an instance of the given
    class. You can use the ``rep`` argument to specify what an instance of this
    class should be called. If you don't do this it will default to ``an
    instance of {cls.__name__}``.
    """

    def __init__(self, cls, rep=None):
        if rep is None:
            rep = 'an instance of {}'.format(cls.__name__)
        self._cls = cls
        self._valid_exp = Explanation(
            True, 'instance_of', 'data is {}'.format(rep)
        )
        self._not_valid_exp = Explanation(
            False, 'not_instance_of', 'data is not {}'.format(rep)
        )

    def _evaluate(self, data, explain, context):
        return (
            (self._valid_exp if explain else True)
            if isinstance(data, context(self._cls)) else
            (self._not_valid_exp if explain else False)
        )
