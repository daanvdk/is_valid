import json


def is_transformed(transform, predicate, *args, exceptions=[
    Exception
], msg='data can\'t be transformed', **kwargs):
    def is_valid(data, explain=False, include=False):
        try:
            data = transform(data, *args, **kwargs)
        except Exception as e:
            if not any(isinstance(e, exc) for exc in exceptions):
                raise e
            return (
                (False, msg, None) if explain else (False, None)
            ) if include else (
                (False, msg) if explain else False
            )
        return ((
            predicate(data, explain=True) + (data,)
        ) if explain else (
            predicate(data), data
        )) if include else predicate(data, explain=explain)
    return is_valid


def is_json(predicate, *args, loader=json.loads, **kwargs):
    return is_transformed(loader, predicate, *args, exceptions=[
        json.JSONDecodeError
    ], msg='data is not valid json', **kwargs)
