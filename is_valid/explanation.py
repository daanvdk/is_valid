import json
from collections import defaultdict


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


def merge(*explanations):
    if any(not explanation for explanation in explanations):
        explanations = [
            explanation
            for explanation in explanations
            if not explanation
        ]
        valid = False
    else:
        valid = True

    details = defaultdict(list)
    merged_explanations = []

    for explanation in explanations:
        if explanation.code in ['dict_where', 'not_dict_where']:
            for key, value in explanation.details.items():
                details[key].append(value)
        elif explanation.code in ['all_hold', 'not_all_hold']:
            merged_explanations.extend(explanation.details)
        else:
            merged_explanations.append(explanation)

    if details:
        merged_explanations.append(Explanation(
            valid,
            'dict_where' if valid else 'not_dict_where',
            (
                'data is a dict where all the given predicates hold'
                if valid else
                'data is not a dict where all the given predicates hold'
            ),
            {
                key: merge(*explanations)
                for key, explanations in details.items()
            },
        ))

    if not merged_explanations:
        raise ValueError('Cannot merge 0 explanations')

    if len(merged_explanations) == 1:
        return merged_explanations[0]

    return Explanation(
        valid,
        'all_hold' if valid else 'not_all_hold',
        (
            'all of the given predicates hold'
            if valid else
            'at least one of the given predicates does not hold'
        ),
        merged_explanations,
    )


class Explanation:

    def __init__(self, valid, code, message, details=None):
        self.valid = valid
        self.code = code
        self.message = message
        self.details = details

    def summary(self):
        res = 'Data is valid.\n' if self.valid else 'Data is not valid.\n'
        for path, subexplanation in self.by_path():
            if path:
                prefix = '[{}] '.format(':'.join(map(repr, path)))
            else:
                prefix = ''
            res += '\n' + subexplanation.__summary(prefix)
        return res

    def __summary(self, prefix=''):
        if hasattr(self, 'data'):
            if self.message.startswith('data '):
                message = '{!r} {}' .format(self.data, self.message[4:])
            else:
                message = '{} ({!r})' .format(self.message, self.data)
        else:
            message = self.message
        return prefix + message

    def __str__(self):
        return self.__summary()

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

    def list(
        self, include_valid=False, include_details=True, include_data=True,
        prefix=(),
    ):
        return [
            {
                **explanation.dict(
                    include_valid=include_valid,
                    include_details=include_details,
                    include_data=include_data,
                ),
                'path': path,
            }
            for path, explanation in self.by_path(prefix)
        ]

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

    def __add__(self, other):
        if not isinstance(other, Explanation):
            raise TypeError
        return merge(self, other)
