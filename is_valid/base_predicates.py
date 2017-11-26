from .explanation import Explanation
from .expression_predicates import is_eq


def is_fixed(valid, code, message):
    """
    Generates a predicate that returns a certain value for valid, code, and
    message that it will always return regardless of what data you put into
    it.
    """
    return lambda _, explain=False: (
        Explanation(valid, code, message) if explain else valid
    )


#: A predicate that regardless of what data you put into will always consider
#: it valid with the explanation 'data is something'. This is the weakest
#: predicate possible.
is_something = is_fixed(True, 'is_something', 'data is something')
#: A predicate that regardless of what data you put into will always consider
#: it invalid with the explanation 'data is something'. This is the strongest
#: predicate possible.
is_nothing = is_fixed(False, 'is_something', 'data is something')


def is_not(predicate):
    """
    Generates the inverse of a given predicate. So if the given predicate would
    consider the data valid the generated predicate will consider it invalid,
    and the other way around. It reuses the explanation of the given predicate.
    """
    if not callable(predicate):
        predicate = is_eq(predicate)

    return lambda data, explain=False: (
        ~predicate(data, explain=True) if explain else not predicate(data)
    )
