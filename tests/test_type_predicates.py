from unittest import TestCase
from datetime import datetime, date, time, timedelta
from decimal import Decimal

from hypothesis import given

from is_valid import is_iterable, is_instance, is_str, is_int, is_float,\
    is_bool, is_list, is_dict, is_set, is_tuple, is_datetime, is_date,\
    is_time, is_timedelta, is_number, is_json, is_byte, is_bytes, is_decimal

from .utils import classes, scalars, json_data, invalid_json_data


class TestTypePredicates(TestCase):

    @given(classes, scalars)
    def test_is_instance(self, cls, value):
        pred = is_instance(cls)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), isinstance(value, cls))

    @given(scalars)
    def test_is_iterable(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_iterable(value), is_iterable.explain(value).valid
            )
        with self.subTest('pred correct'):
            self.assertEqual(
                is_iterable(value),
                isinstance(value, (list, dict, set, tuple, str, bytes))
            )

    @given(scalars)
    def test_is_str(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_str(value), is_str.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(is_str(value), isinstance(value, str))

    @given(scalars)
    def test_is_int(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_int(value), is_int.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(is_int(value), isinstance(value, int))

    @given(scalars)
    def test_is_float(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_float(value), is_float.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(is_float(value), isinstance(value, float))

    @given(scalars)
    def test_is_decimal(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_decimal(value), is_decimal.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(is_decimal(value), isinstance(value, Decimal))

    @given(scalars)
    def test_is_bool(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_bool(value), is_bool.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(is_bool(value), isinstance(value, bool))

    @given(scalars)
    def test_is_list(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_list(value), is_list.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(is_list(value), isinstance(value, list))

    @given(scalars)
    def test_is_dict(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_dict(value), is_dict.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(is_dict(value), isinstance(value, dict))

    @given(scalars)
    def test_is_set(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_set(value), is_set.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(is_set(value), isinstance(value, set))

    @given(scalars)
    def test_is_tuple(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_tuple(value), is_tuple.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(is_tuple(value), isinstance(value, tuple))

    @given(scalars)
    def test_is_datetime(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_datetime(value), is_datetime.explain(value).valid
            )
        with self.subTest('pred correct'):
            self.assertEqual(is_datetime(value), isinstance(value, datetime))

    @given(scalars)
    def test_is_date(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_date(value), is_date.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(is_date(value), isinstance(value, date))

    @given(scalars)
    def test_is_time(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_time(value), is_time.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(is_time(value), isinstance(value, time))

    @given(scalars)
    def test_is_timedelta(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_timedelta(value), is_timedelta.explain(value).valid
            )
        with self.subTest('pred correct'):
            self.assertEqual(is_timedelta(value), isinstance(value, timedelta))

    @given(scalars)
    def test_is_number(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_number(value), is_number.explain(value).valid
            )
        with self.subTest('pred correct'):
            self.assertEqual(is_number(value), isinstance(value, (int, float, Decimal)))

    @given(scalars)
    def test_is_byte(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_byte(value), is_byte.explain(value).valid
            )
        with self.subTest('pred correct'):
            self.assertEqual(
                is_byte(value),
                isinstance(value, int) and 0 <= value and value <= 255
            )

    @given(scalars)
    def test_is_bytes(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_bytes(value), is_bytes.explain(value).valid
            )
        with self.subTest('pred correct'):
            self.assertEqual(is_bytes(value), isinstance(value, bytes))

    def test_is_json_valid_data(self):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_json(json_data), is_json.explain(json_data).valid
            )
        with self.subTest('pred correct'):
            self.assertTrue(is_json(json_data))

    def test_is_json_invalid_data(self):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_json(invalid_json_data),
                is_json.explain(invalid_json_data).valid
            )
        with self.subTest('pred correct'):
            self.assertFalse(is_json(invalid_json_data))
