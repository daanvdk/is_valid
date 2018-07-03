from .is_instance import is_instance


#: A predicate that checks if the data is bytes.
is_bytes = is_instance(bytes, rep='bytes')
