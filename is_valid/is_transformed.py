from .base import Predicate
from .to_pred import to_pred
from .is_fixed import is_fixed


is_transformable = is_fixed(
    True, 'transformable', 'data can be transformed'
)

is_not_transformable = is_fixed(
    False, 'not_transformable', 'data can not be transformed'
)


class is_transformed(Predicate):
    """
    Generates a predicate that checks if the data is valid according to some
    predicate after a function has been applied to the data. If this function
    throws an exception the predicate will consider the data invalid.

    With the ``exceptions`` parameter you can limit the exceptions that the
    predicate catches. With the ``msg`` parameter you can specify what the
    explanation should be when the predicate catches an exception.

    All other arguments provided will be passed on to the transform function.
    """

    def __init__(
        self, transform, success=is_transformable, fail=is_not_transformable,
        exceptions=[Exception],
    ):
        self._transform = transform
        self._success = to_pred(success)
        self._fail = to_pred(fail)
        self._exceptions = exceptions

    def _evaluate(self, data, explain, context):
        try:
            data = self._transform(data)
        except Exception as e:
            if not any(isinstance(e, exc) for exc in self._exceptions):
                raise e
            return self._fail(data, explain, context)
        else:
            return self._success(data, explain, context)
