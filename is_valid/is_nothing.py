from .is_fixed import is_fixed


#: A predicate that regardless of what data you put into will always consider
#: it invalid with the explanation 'Data is something.'. This is the strongest
#: predicate possible.
is_nothing = is_fixed(False, 'is_something', 'data is something')
