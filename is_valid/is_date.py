from .is_instance import is_instance
from datetime import date


#: A predicate that checks if the data is a date.
is_date = is_instance(date, rep='a date')
