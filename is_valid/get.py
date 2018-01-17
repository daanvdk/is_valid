def identity(value):
    return value


class Get(object):

    def __init__(self, key, transform=identity, rep=None):
        self._key = key
        self._transform = transform
        self._rep = str(key) if rep is None else rep

    def __repr__(self):
        return self._rep
