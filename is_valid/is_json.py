from .is_json_where import is_json_where
from .is_fixed import is_fixed


is_json = is_json_where(is_fixed(True, 'json', 'data is json'))
