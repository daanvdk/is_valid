from .base import instantiate
from .is_int import is_int
from .is_in_range import is_in_range


@instantiate
class is_byte(is_in_range):

    prerequisites = [is_int]

    def __init__(self):
        super().__init__(0, 255, stop_in=True)
