import json


def _dictify(value, include_valid):
    if isinstance(value, Explanation):
        return value.dict(include_valid=include_valid)
    if isinstance(value, list):
        return [_dictify(v, include_valid) for v in value]
    if isinstance(value, dict):
        return {k: _dictify(v, include_valid) for k, v in value.items()}
    if isinstance(value, tuple):
        return tuple(_dictify(v, include_valid) for v in value)
    return value


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

    def dict(self, include_valid=False, include_details=True):
        res = {
            'code': self.code,
            'message': self.message,
        }
        if include_details and self.details is not None:
            res['details'] = _dictify(self.details, include_valid)
        if include_valid:
            res['valid'] = self.valid
        return res

    def json(self, *args, include_valid=False, include_details=True, **kwargs):
        return json.dumps(self.dict(
            include_valid=include_valid,
            include_details=include_details,
        ), *args, **kwargs)
