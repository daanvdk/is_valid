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
        subexplanations = self.by_path()
        # So we want to call __repr if and only if we have exactly one
        # subexplanation with an empty path, otherwise we call __repr_by_path
        path, _ = next(subexplanations)
        if path != []:
            # Not an empty path
            return self.__repr_by_path()
        try:
            next(subexplanations)
        except StopIteration:
            return self.__repr()
        else:
            # Multiple subexplanations
            return self.__repr_by_path()

    def __repr(self, prefix=''):
        res = '{}{}: {}'.format(prefix, self.code, self.message)
        if hasattr(self, 'data'):
            res += ', {!r}'.format(self.data)
        return res

    def __repr_by_path(self):
        return '\n'.join(
            subexplanation.__repr('[{}] '.format(':'.join(map(repr, path))))
            for path, subexplanation in self.by_path()
        )

    def __bool__(self):
        return self.valid

    def __invert__(self):
        return Explanation(
            not self.valid, self.code, self.message, self.details
        )

    def dict(
        self, include_valid=False, include_details=True, include_data=True,
    ):
        res = {
            'code': self.code,
            'message': self.message,
        }
        if include_data and hasattr(self, 'data'):
            res['data'] = self.data
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

    def copy(self, **kwargs):
        res = Explanation(
            valid=kwargs.pop('valid', self.valid),
            code=kwargs.pop('code', self.code),
            message=kwargs.pop('message', self.message),
            details=kwargs.pop('details', self.details),
        )

        if hasattr(self, 'data'):
            res.data = self.data

        for key, value in kwargs.items():
            setattr(res, key, value)

        return res

    def by_path(self, prefix=()):
        if self.code in [
            'all_hold', 'not_all_hold',
            'none_hold', 'multiple_hold',
        ]:
            for subexp in self.details:
                yield from subexp.by_path(prefix)
        elif self.code in ['dict_of', 'not_dict_of']:
            for key, subexp in self.details.items():
                for subsubexp in subexp.values():
                    yield from subsubexp.by_path((*prefix, key))
        elif self.code in [
            'dict_where', 'not_dict_where',
            'iterable_of', 'not_iterable_of',
            'iterable_where', 'not_iterable_where',
            'object_where', 'not_object_where',
            'subdict_where', 'not_subdict_where',
            'set_of', 'not_set_of',
            'superdict_where', 'not_superdict_where',
        ]:
            for key, subexp in self.details.items():
                yield from subexp.by_path((*prefix, key))
        elif self.code == 'one_holds':
            yield prefix, self.details
        else:
            yield prefix, self
