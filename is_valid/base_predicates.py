def is_fixed(valid, explanation):
    return lambda _, explain=False: (valid, explanation) if explain else valid


is_something = is_fixed(True, 'data is something')
is_nothing = is_fixed(False, 'data is something')


def is_not(predicate):
    def is_valid(data, explain=False):
        if not explain:
            return not predicate(data)
        valid, explanation = predicate(data, explain=True)
        return (not valid, explanation)
    return is_valid
