from .is_instance import is_instance
from datetime import time


#: A predicate that checks if the data is a time.
is_time = is_instance(time, rep='a time')
