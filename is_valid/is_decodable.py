from .is_decodable_where import is_decodable_where
from .is_fixed import is_fixed


class is_decodable(is_decodable_where):

    def __init__(self, encoding='utf-8', errors='strict'):
        super().__init__(
            is_fixed(True, 'decodable', 'data is decodable'),
            encoding, errors,
        )
