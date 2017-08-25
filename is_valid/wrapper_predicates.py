import json


def is_transformed(
    transform, validator, *args,
    exceptions=[Exception], msg='data can\'t be transformed', **kwargs
):
    def is_valid(data, detailed=False):
        try:
            data = transform(data, *args, **kwargs)
        except Exception as e:
            if not any(isinstance(e, cls) for cls in exceptions):
                raise e
            return (False, msg) if detailed else False
        return validator(data, detailed=detailed)
    return is_valid


def is_json(validator, *args, **kwargs):
    return is_transformed(
        json.loads, validator,
        *args,
        exceptions=[json.JSONDecodeError], msg='data is not valid json',
        **kwargs
    )
