import json

from .is_decodable_where import is_decodable_where
from .is_json_where import is_json_where


class is_decodable_json_where(is_decodable_where):

    def __init__(
        self, predicate, loader=json.loads, encoding='utf-8', errors='strict'
    ):
        return super().__init__(
            is_json_where(predicate, loader=loader),
            encoding=encoding,
            errors=errors,
        )
