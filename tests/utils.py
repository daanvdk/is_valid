import re
from datetime import datetime, date, time, timedelta

import hypothesis.strategies as hs


varying = hs.one_of(hs.integers(), hs.floats(), hs.text(), hs.booleans())
for _ in range(3):
    varying = hs.one_of(
        varying,
        hs.lists(varying, max_size=10),
    )

numbers = hs.one_of(hs.integers(), hs.floats())


regexs = [r'\d+', r'^foo(bar){3}$', re.compile(r'^FoOBaR$', flags=re.I)]


@hs.composite
def regex_with_match(draw):
    regex = draw(hs.sampled_from(regexs))
    match = draw(hs.from_regex(regex))
    return (regex, match)


scalars = hs.one_of(
    hs.text(), hs.integers(), hs.floats(), hs.booleans(),
    hs.lists(hs.integers()), hs.dictionaries(hs.integers(), hs.integers()),
    hs.sets(hs.integers()), hs.tuples(hs.integers()), hs.datetimes(),
    hs.dates(), hs.times(), hs.timedeltas(), hs.binary(),
)
classes = hs.sampled_from([
    str, int, float, bool, list, dict, set, tuple, datetime, date, time,
    timedelta
])


dicts = hs.one_of(
    hs.fixed_dictionaries({
        'foo': hs.booleans(),
        'bar': hs.booleans()
    }),
    hs.fixed_dictionaries({
        'foo': hs.booleans()
    }),
    hs.fixed_dictionaries({
        'foo': hs.booleans(),
        'bar': hs.booleans(),
        'baz': hs.booleans()
    }),
    hs.fixed_dictionaries({
        'foo': hs.booleans(),
        'baz': hs.booleans()
    }),
    hs.booleans()
)
correct_dict = {'foo': True, 'bar': False}


lists = hs.one_of(
    hs.lists(hs.booleans(), min_size=0, max_size=4),
    hs.booleans()
)
correct_list = [True, False]


@hs.composite
def tuples(draw):
    list_ = draw(lists)
    return tuple(list_) if isinstance(list_, list) else list_


correct_tuple = (True, False)


class FooBar(object):
    def __init__(self, foo, bar):
        self.foo, self.bar = foo, bar


class FooBarBaz(object):
    def __init__(self, foo, bar, baz):
        self.foo, self.bar, self.baz = foo, bar, baz


class Foo(object):
    def __init__(self, foo):
        self.foo = foo


class FooBaz(object):
    def __init__(self, foo, baz):
        self.foo, self.baz = foo, baz


@hs.composite
def object_with_attrs(draw, *attrs):
    return draw(hs.sampled_from([
        FooBar(draw(hs.booleans()), draw(hs.booleans())),
        FooBarBaz(
            draw(hs.booleans()), draw(hs.booleans()), draw(hs.booleans())
        ),
        Foo(draw(hs.booleans())),
        FooBaz(draw(hs.booleans()), draw(hs.booleans()))
    ]))


objects = hs.one_of(
    object_with_attrs('foo', 'bar'),
    object_with_attrs('foo', 'bar', 'baz'),
    object_with_attrs('foo'),
    object_with_attrs('foo', 'baz'),
    hs.booleans()
)


json_data = """
{
    "foo": [
        {
            "bar": true,
            "baz": "some string"
        },
        {
            "bar": true,
            "baz": "some string"
        },
        {
            "bar": true,
            "baz": "some string"
        }
    ],
    "bar": 1234567890
}
"""
incorrect_json_data = """
{
    "foo": [
        {
            "bar": true,
            "baz": null
        },
        {
            "bar": true,
            "baz": "some string"
        },
        {
            "bar": true,
            "baz": "some string"
        }
    ],
    "bar": 1234567890
}
"""
invalid_json_data = """
{
    "foo": [
        {
            "bar": truee,
            "baz": "some string"
        },
        {
            "bar": true,
            "baz": "some string"
        },
        {
            "bar": true,
            "baz": "some string"
        }
    ],
    "bar": 1234567890
}
"""


decode_utf8_data = (
    b'\xd9\xa9(-\xcc\xae\xcc\xae-\xcc\x83)\xdb\xb6 \xd9\xa9(\xe2\x97\x8f\xcc'
    b'\xae\xcc\xae\xe2\x80\xa2\xcc\x83)\xdb\xb6 \xd9\xa9(\xcd\xa1\xe0\xb9\x8f'
    b'\xcc\xaf\xcd\xa1\xe0\xb9\x8f)\xdb\xb6 \xd9\xa9(-\xcc\xae\xcc\xae\xe2\x80'
    b'\xa2\xcc\x83).'
)
decode_utf32_data = (
    b'\xff\xfe\x00\x00i\x06\x00\x00(\x00\x00\x00-\x00\x00\x00.\x03\x00\x00.'
    b'\x03\x00\x00-\x00\x00\x00\x03\x03\x00\x00)\x00\x00\x00\xf6\x06\x00\x00 '
    b'\x00\x00\x00i\x06\x00\x00(\x00\x00\x00\xcf%\x00\x00.\x03\x00\x00.\x03'
    b'\x00\x00" \x00\x00\x03\x03\x00\x00)\x00\x00\x00\xf6\x06\x00\x00 \x00\x00'
    b'\x00i\x06\x00\x00(\x00\x00\x00a\x03\x00\x00O\x0e\x00\x00/\x03\x00\x00a'
    b'\x03\x00\x00O\x0e\x00\x00)\x00\x00\x00\xf6\x06\x00\x00 \x00\x00\x00i\x06'
    b'\x00\x00(\x00\x00\x00-\x00\x00\x00.\x03\x00\x00.\x03\x00\x00" \x00\x00'
    b'\x03\x03\x00\x00)\x00\x00\x00.\x00\x00\x00'
)
decode_invalid_data = b'\x01\x03\x05\xea'
