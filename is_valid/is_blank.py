from .utils import explain


def blank(value):
    return not value


is_blank = explain(
    blank,
    code='blank',
    message_valid='data is blank',
    message_invalid='data is not blank',
)
is_not_blank = ~is_blank
