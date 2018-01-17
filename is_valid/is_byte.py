from .is_if import is_if
from .is_int import is_int
from .is_in_range import is_in_range


is_byte = is_if(is_int, is_in_range(0, 255, stop_in=True), else_valid=False)
