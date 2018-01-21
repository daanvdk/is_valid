from .is_transformed import is_transformed
from .is_fixed import is_fixed
from json import loads


class is_json_where(is_transformed):
    """
    Generates a predicate that checks if the data is valid according to some
    predicate after it has been decoded as JSON. The predicate considers the
    data invalid if it is invalid JSON.

    With the ``loader`` parameter you can specify a different loader than the
    default JSON loader.

    All other arguments provided will be passed on to the JSON loader.
    """

    def __init__(self, predicate, loader=loads):
        super().__init__(
            loader, predicate,
            is_fixed(False, 'not_json', 'Data is not valid json.'),
            exceptions=[ValueError],
        )
