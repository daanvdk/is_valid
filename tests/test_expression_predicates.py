from unittest import TestCase
from itertools import product
import re

from is_valid import is_eq, is_neq, is_lt, is_leq, is_gt, is_geq, is_in,\
    is_not_in, is_none, is_not_none, is_null, is_not_null, is_in_range,\
    is_not_in_range, is_match, is_not_match


class TestExpressionPredicates(TestCase):

    def test_equivalence(self):
        values = [1, 2, 3, '1', '2', '3', [1, 2, 3], ['1', '2', '3']]
        for name, predicate, func in [
            ('is_eq', is_eq, lambda a, b: b == a),
            ('is_neq', is_neq, lambda a, b: b != a),
        ]:
            for a in values:
                is_func_a = predicate(a)
                for b in values:
                    with self.subTest('{}: non-detail == detail'.format(name)):
                        self.assertEqual(
                            is_func_a(b),
                            is_func_a(b, detailed=True)[0]
                        )
                    with self.subTest('{}: {!r}, {!r}'.format(name, b, a)):
                        self.assertEqual(is_func_a(b), func(a, b))

    def test_comparison(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for name, predicate, func in [
            ('is_lt', is_lt, lambda a, b: b < a),
            ('is_leq', is_leq, lambda a, b: b <= a),
            ('is_gt', is_gt, lambda a, b: b > a),
            ('is_geq', is_geq, lambda a, b: b >= a),
        ]:
            for a in values:
                is_func_a = predicate(a)
                for b in values:
                    with self.subTest('{}: non-detail == detail'.format(name)):
                        self.assertEqual(
                            is_func_a(b),
                            is_func_a(b, detailed=True)[0]
                        )
                    with self.subTest('{}: {!r}, {!r}'.format(name, b, a)):
                        self.assertEqual(is_func_a(b), func(a, b))

    def test_range(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for name, predicate, start_in, stop_in, func in [
            ('is_in_range', is_in_range, False, False,
                lambda a, b, c: a < b < c),
            ('is_in_range', is_in_range, False, True,
                lambda a, b, c: a < b <= c),
            ('is_in_range', is_in_range, True, False,
                lambda a, b, c: a <= b < c),
            ('is_in_range', is_in_range, True, True,
                lambda a, b, c: a <= b <= c),
            ('is_not_in_range', is_not_in_range, False, False,
                lambda a, b, c: b <= a or c <= b),
            ('is_not_in_range', is_not_in_range, False, True,
                lambda a, b, c: b <= a or c < b),
            ('is_not_in_range', is_not_in_range, True, False,
                lambda a, b, c: b < a or c <= b),
            ('is_not_in_range', is_not_in_range, True, True,
                lambda a, b, c: b < a or c < b),
        ]:
            for start, stop in product(values, values):
                is_func = predicate(
                    start, stop,
                    start_in=start_in, stop_in=stop_in
                )
                for value in values:
                    with self.subTest('{}: non-detail == detail'.format(name)):
                        self.assertEqual(
                            is_func(value),
                            is_func(value, detailed=True)[0]
                        )
                    with self.subTest('{}: {}, {}, {!r}, {!r}'.format(
                        name, start, start_in, stop, stop_in, value
                    )):
                        self.assertEqual(
                            is_func(value),
                            func(start, value, stop)
                        )

    def test_collection(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        collections = [set([1, 2, 3]), set([4, 5, 6]), set([7, 8, 9])]
        for name, predicate, func in [
            ('is_in', is_in, lambda a, b: b in a),
            ('is_not_in', is_not_in, lambda a, b: b not in a),
        ]:
            for a in collections:
                is_func_a = predicate(a)
                for b in values:
                    with self.subTest('{}: non-detail == detail'.format(name)):
                        self.assertEqual(
                            is_func_a(b),
                            is_func_a(b, detailed=True)[0]
                        )
                    with self.subTest('{}: {!r}, {!r}'.format(name, b, a)):
                        self.assertEqual(is_func_a(b), func(a, b))

    def test_nullability(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, None]
        for name, predicate, func in [
            ('is_none', is_none, lambda a: a is None),
            ('is_not_none', is_not_none, lambda a: a is not None),
            ('is_null', is_null, lambda a: a is None),
            ('is_not_null', is_not_null, lambda a: a is not None),
        ]:
            for a in values:
                with self.subTest('{}: non-detail == detail'.format(name)):
                    self.assertEqual(
                        predicate(a),
                        predicate(a, detailed=True)[0]
                    )
                with self.subTest('{}: {!r}'.format(name, a)):
                    self.assertEqual(predicate(a), func(a))

    def test_patterns(self):
        patterns = [re.compile(r'^\d+$'), r'^[a-z]+$']
        values = ['123', 'abc', 'ABC', '123abc', None, 123]
        for name, predicate, func in [
            ('is_match', is_match,
                lambda a, b: isinstance(b, str) and bool(a.match(b))),
            ('is_not_match', is_not_match,
                lambda a, b: isinstance(b, str) and not a.match(b)),
        ]:
            for pattern in patterns:
                is_func = predicate(pattern)
                if isinstance(pattern, str):
                    pattern = re.compile(pattern)
                for value in values:
                    with self.subTest('{}: non-detail == detail'.format(name)):
                        self.assertEqual(
                            is_func(value),
                            is_func(value, detailed=True)[0]
                        )
                    with self.subTest('{}: {!r}, {!r}'.format(
                        name, value, pattern.pattern
                    )):
                        self.assertEqual(is_func(value), func(pattern, value))
