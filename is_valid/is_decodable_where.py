from .is_transformed import is_transformed
from .is_bytes import is_bytes
from .is_fixed import is_fixed


class is_decodable_where(is_transformed):

    prerequisites = [is_bytes]

    def __init__(self, predicate, encoding='utf-8', errors='strict'):
        super().__init__(
            lambda s: s.decode(encoding, errors), predicate,
            is_fixed(False, 'not_decodable', 'data is not decodable'),
            exceptions=[UnicodeDecodeError],
        )
