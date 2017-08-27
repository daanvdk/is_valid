def is_fixed(valid, explanation):
    """
    Generates a predicate that returns a certain value for valid and
    explanation that it will always return regardless of what data you put into
    it.
    """
    return lambda _, explain=False: (valid, explanation) if explain else valid


#: A predicate that regardless of what data you put into it will always return
#:
is_something = is_fixed(True, 'data is something')
#: is_nothing
is_nothing = is_fixed(False, 'data is something')


def is_not(predicate):
    def is_valid(data, explain=False):
        if not explain:
            return not predicate(data)
        valid, explanation = predicate(data, explain=True)
        return (not valid, explanation)
    return is_valid
