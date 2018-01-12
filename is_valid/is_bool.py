from .is_instance import is_instance


#: A predicate that checks if the data is a boolean.
is_bool = is_instance(bool, rep='a bool')
