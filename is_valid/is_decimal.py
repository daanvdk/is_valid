from .is_instance import is_instance
from decimal import Decimal


#: A predicate that checks if the data is a decimal.
is_decimal = is_instance(Decimal, rep='a decimal')
