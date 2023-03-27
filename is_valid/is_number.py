from .is_instance import is_instance
from decimal import Decimal

#: A predicate that checks if the data is a number.
is_number = is_instance((int, float, Decimal), rep='a number')
