import json


class Explanation:

    def __init__(self, valid, code, message, details=None):
        self.valid = valid
        self.code = code
        self.message = message
        self.details = details

    def __str__(self):
        return '{}: {}'.format(self.code, self.message)

    def __repr__(self):
        return (
            'Explanation(valid={0.valid!r}, code={0.code!r}, '
            'message={0.message!r}, details={0.details!r})'
        ).format(self)

    def __bool__(self):
        return self.valid

    def __invert__(self):
        return Explanation(
            not self.valid, self.code, self.message, self.details
        )

    def dict(self, include_valid=False):
        res = {
            'code': self.code,
            'message': self.message,
        }
        if self.details is not None:
            res['details'] = self.details
        if include_valid:
            res['valid'] = self.valid
        return res

    def json(self, *args, include_valid=False, **kwargs):
        return json.dumps(
            self.dict(include_valid=include_valid), *args, **kwargs
        )
