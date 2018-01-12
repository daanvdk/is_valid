from .is_instance import is_instance


#: A predicate that checks if the data is a tuple.
is_tuple = is_instance(tuple, rep='a tuple')
