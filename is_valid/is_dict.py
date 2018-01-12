from .is_instance import is_instance


#: A predicate that checks if the data is a dictionary.
is_dict = is_instance(dict, rep='a dict')
