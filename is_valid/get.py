def identity(value):
    return value


class Get(object):

    def __init__(self, key, transform=identity, rep=None):
        self._key = key
        self._transform = transform
        self._rep = rep

    def __repr__(self):
        return super().__repr__() if self._rep is None else self._rep
