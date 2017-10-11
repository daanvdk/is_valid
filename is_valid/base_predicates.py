def is_fixed(valid, explanation):
    """
    Generates a predicate that returns a certain value for valid and
    explanation that it will always return regardless of what data you put into
    it.
    """
    return lambda _, explain=False: (valid, explanation) if explain else valid


#: A predicate that regardless of what data you put into will always consider
#: it valid with the explanation 'data is something'. This is the weakest
#: predicate possible.
is_something = is_fixed(True, 'data is something')
#: A predicate that regardless of what data you put into will always consider
#: it invalid with the explanation 'data is something'. This is the strongest
#: predicate possible.
is_nothing = is_fixed(False, 'data is something')


def is_not(predicate):
    """
    Generates the inverse of a given predicate. So if the given predicate would
    consider the data valid the generated predicate will consider it invalid,
    and the other way around. It reuses the explanation of the given predicate.
    """
    def is_valid(data, explain=False):
        if not explain:
            return not predicate(data)
        valid, explanation = predicate(data, explain=True)
        return (not valid, explanation)
    return is_valid
