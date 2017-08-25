def is_anything(data, detailed=False):
    return (True, None) if detailed else True


def is_nothing(data, detailed=False):
    return (False, 'data is not nothing') if detailed else False
