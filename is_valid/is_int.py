from .is_instance import is_instance


#: A predicate that checks if the data is an integer.
is_int = is_instance(int, rep='an int')
