from .is_instance import is_instance


#: A predicate that checks if the data is a set.
is_set = is_instance(set, rep='a set')
