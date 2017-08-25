from .negation_predicates import is_not


def is_something(data, explain=False):
    return (True, 'data is something') if explain else True


is_nothing = is_not(is_something)
