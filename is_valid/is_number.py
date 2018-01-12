from .is_instance import is_instance

#: A predicate that checks if the data is a number.
is_number = is_instance((int, float), rep='a number')
