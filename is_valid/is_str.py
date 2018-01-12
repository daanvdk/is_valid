from .is_instance import is_instance


#: A predicate that checks if the data is a string.
is_str = is_instance(str, rep='a str')
