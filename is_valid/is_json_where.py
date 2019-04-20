from .is_transformed import is_transformed
from .is_str import is_str
from .is_fixed import is_fixed
import json


class is_json_where(is_transformed):

    prerequisites = [is_str]

    def __init__(self, predicate, loader=json.loads):
        super().__init__(
            loader, predicate,
            is_fixed(False, 'not_json', 'data is not json'),
            exceptions=[ValueError],
        )
