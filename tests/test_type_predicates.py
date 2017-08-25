from unittest import TestCase
from datetime import datetime, date, time, timedelta

from hypothesis import given
import hypothesis.strategies as hs

from is_valid import is_iterable, is_instance, is_str, is_int, is_float,\
    is_bool, is_list, is_dict, is_set, is_tuple, is_datetime, is_date,\
    is_time, is_timedelta, is_number

scalars = hs.one_of(
    hs.text(), hs.integers(), hs.floats(), hs.booleans(),
    hs.lists(hs.integers()), hs.dictionaries(hs.integers(), hs.integers()),
    hs.sets(hs.integers()), hs.tuples(hs.integers()), hs.datetimes(),
    hs.dates(), hs.times(), hs.timedeltas()
)
classes = hs.sampled_from([
    str, int, float, bool, list, dict, set, tuple, datetime, date, time,
    timedelta
])


class TestTypePredicates(TestCase):

    @given(classes, scalars)
    def test_is_instance(self, cls, value):
        pred = is_instance(cls)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred(value, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), isinstance(value, cls))

    @given(scalars)
    def test_is_iterable(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_iterable(value), is_iterable(value, explain=True)[0]
            )
        with self.subTest('pred correct'):
            self.assertEqual(
                is_iterable(value),
                isinstance(value, (list, dict, set, tuple, str))
            )

    @given(scalars)
    def test_is_str(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_str(value), is_str(value, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(is_str(value), isinstance(value, str))

    @given(scalars)
    def test_is_int(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_int(value), is_int(value, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(is_int(value), isinstance(value, int))

    @given(scalars)
    def test_is_float(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_float(value), is_float(value, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(is_float(value), isinstance(value, float))

    @given(scalars)
    def test_is_bool(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_bool(value), is_bool(value, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(is_bool(value), isinstance(value, bool))

    @given(scalars)
    def test_is_list(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_list(value), is_list(value, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(is_list(value), isinstance(value, list))

    @given(scalars)
    def test_is_dict(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_dict(value), is_dict(value, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(is_dict(value), isinstance(value, dict))

    @given(scalars)
    def test_is_set(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_set(value), is_set(value, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(is_set(value), isinstance(value, set))

    @given(scalars)
    def test_is_tuple(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_tuple(value), is_tuple(value, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(is_tuple(value), isinstance(value, tuple))

    @given(scalars)
    def test_is_datetime(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_datetime(value), is_datetime(value, explain=True)[0]
            )
        with self.subTest('pred correct'):
            self.assertEqual(is_datetime(value), isinstance(value, datetime))

    @given(scalars)
    def test_is_date(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_date(value), is_date(value, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(is_date(value), isinstance(value, date))

    @given(scalars)
    def test_is_time(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_time(value), is_time(value, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(is_time(value), isinstance(value, time))

    @given(scalars)
    def test_is_timedelta(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_timedelta(value), is_timedelta(value, explain=True)[0]
            )
        with self.subTest('pred correct'):
            self.assertEqual(is_timedelta(value), isinstance(value, timedelta))

    @given(scalars)
    def test_is_number(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_number(value), is_number(value, explain=True)[0]
            )
        with self.subTest('pred correct'):
            self.assertEqual(is_number(value), isinstance(value, (int, float)))
