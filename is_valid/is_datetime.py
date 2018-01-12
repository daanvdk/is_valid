from .is_instance import is_instance
from datetime import datetime


#: A predicate that checks if the data is a datetime.
is_datetime = is_instance(datetime, rep='a datetime')
