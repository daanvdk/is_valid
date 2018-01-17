from .base import Predicate
from .explanation import Explanation
from .is_eq import to_pred


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
        self, transform, predicate, *args,
        exceptions=[Exception],
        code='not_transformable', message='Data can\'t be transformed.',
        **kwargs
    ):
        self._transform = transform
        self._predicate = to_pred(predicate)
        self._exceptions = exceptions
        self._not_valid_exp = Explanation(
            False, 'not_{}'.format(code), message
        )
        self._args = args
        self._kwargs = kwargs

    def _evaluate(self, data, explain, context):
        try:
            data = self._transform(data, *self._args, **self._kwargs)
        except Exception as e:
            if not any(isinstance(e, exc) for exc in self._exceptions):
                raise e
            return self._not_valid_exp if explain else False
        return self._predicate(data, explain, context)
