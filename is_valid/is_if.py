from .base import Predicate
from .to_pred import to_pred
from .is_nothing import is_nothing


class is_if(Predicate):
    """
    Generates a predicate that given a predicate as condition will based on the
    result of this condition on the data evaluate the data with either
    ``if_predicate`` or ``else_predicate``. If else predicate is omitted it
    will use the value of ``else_valid`` for when the condition considers the
    data invalid, as explanation it will reuse the explanation that the
    condition returned.
    """

    def __init__(self, condition, if_predicate, *args, **kwargs):
        else_predicate = None

        if args:
            if len(args) > 1:
                raise TypeError(
                    '__init__() takes 4 positional arguments but {} were given'
                    .format(len(args) + 3)
                )
            else_predicate = to_pred(args[0])

        for key, value in kwargs.items():
            if key != 'else_predicate':
                raise TypeError(
                    '__init__() got an unexpected keyword argument {!r}'
                    .format(key)
                )
            elif else_predicate is not None:
                raise TypeError(
                    '__init__() got multiple values for argument '
                    '\'else_predicate\''
                )
            else_predicate = to_pred(value)

        self._cond = to_pred(condition)
        self._if = to_pred(if_predicate)
        self._else = else_predicate

    def _evaluate(self, data, explain, context):
        res = self._cond(data, explain, context)
        if explain:
            data = res.data
        if res:
            res = self._if(data, explain, context)
        elif self._else is not None:
            res = self._else(data, explain, context)
        else:
            res = ~res if explain else not res
        return res

    @classmethod
    def cases(cls, *cases, default=is_nothing):
        predicate = to_pred(default)
        for cond, then_ in reversed(cases):
            predicate = cls(cond, then_, predicate)
        return predicate
