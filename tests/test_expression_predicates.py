from unittest import TestCase
import re

from hypothesis import given
import hypothesis.strategies as hs

from is_valid import is_eq, is_lt, is_leq, is_gt, is_geq, is_in,\
    is_none, is_null, is_in_range, is_match

from .utils import varying, numbers, regexs, regex_with_match


class TestExpressionPredicates(TestCase):

    @given(varying)
    def test_eq_to_self(self, a):
        pred = is_eq(a)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(a), pred.explain(a).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(a), a == a)

    @given(varying, varying)
    def test_eq(self, a, b):
        pred = is_eq(a)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(b), pred.explain(b).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(b), a == b)

    @given(numbers, numbers)
    def test_lt(self, a, b):
        pred = is_lt(a)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(b), pred.explain(b).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(b), b < a)

    @given(numbers, numbers)
    def test_leq(self, a, b):
        pred = is_leq(a)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(b), pred.explain(b).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(b), b <= a)

    @given(numbers, numbers)
    def test_gt(self, a, b):
        pred = is_gt(a)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(b), pred.explain(b).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(b), b > a)

    @given(numbers, numbers)
    def test_geq(self, a, b):
        pred = is_geq(a)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(b), pred.explain(b).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(b), b >= a)

    @given(numbers, numbers, numbers)
    def test_in_range_ex_ex(self, start, stop, value):
        pred = is_in_range(start, stop, start_in=False, stop_in=False)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), start < value < stop)

    @given(numbers, numbers, numbers)
    def test_in_range_ex_in(self, start, stop, value):
        pred = is_in_range(start, stop, start_in=False, stop_in=True)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), start < value <= stop)

    @given(numbers, numbers, numbers)
    def test_in_range_in_ex(self, start, stop, value):
        pred = is_in_range(start, stop, start_in=True, stop_in=False)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), start <= value < stop)

    @given(numbers, numbers, numbers)
    def test_in_range_in_in(self, start, stop, value):
        pred = is_in_range(start, stop, start_in=True, stop_in=True)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), start <= value <= stop)

    @given(numbers)
    def test_in_set_with_self(self, value):
        pred = is_in(set([value]))
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertTrue(pred(value))

    @given(numbers, hs.sets(numbers, max_size=20))
    def test_in(self, value, collection):
        pred = is_in(collection)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), value in collection)

    @given(varying)
    def test_not_null(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_null(value), is_null.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertFalse(is_null(value))

    def test_null(self):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_null(None), is_null.explain(None).valid)
        with self.subTest('pred correct'):
            self.assertTrue(is_null(None))

    @given(varying)
    def test_not_none(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_none(value), is_none.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertFalse(is_none(value))

    def test_none(self):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(is_none(None), is_none.explain(None).valid)
        with self.subTest('pred correct'):
            self.assertTrue(is_none(None))

    @given(hs.sampled_from(regexs), varying)
    def test_match(self, regex, value):
        pred = is_match(regex)
        if isinstance(regex, str):
            regex = re.compile(regex)
        with self.subTest('{}; explain=True == explain=False'.format(
            regex.pattern
        )):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('{}; pred correct'.format(regex.pattern)):
            self.assertEqual(
                pred(value),
                isinstance(value, str) and bool(regex.search(value))
            )

    @given(regex_with_match())
    def test_matches_match(self, value):
        regex, match = value
        pred = is_match(regex)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(
                pred(value),
                isinstance(value, str) and bool(regex.match(value))
            )
