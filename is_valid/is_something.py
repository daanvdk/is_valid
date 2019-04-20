from .is_fixed import is_fixed


#: A predicate that regardless of what data you put into will always consider
#: it valid with the explanation 'Ddata is something.'. This is the weakest
#: predicate possible.
is_something = is_fixed(True, 'is_something', 'data is something')
