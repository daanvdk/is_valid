def is_not(predicate):
    def is_valid(data, explain=False):
        if not explain:
            return not predicate(data)
        valid, explanation = predicate(data, explain=True)
        return (not valid, explanation)
    return is_valid
