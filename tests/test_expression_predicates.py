from unittest import TestCase
from itertools import product
import re

from is_valid import is_eq, is_neq, is_lt, is_leq, is_gt, is_geq, is_in,\
    is_none, is_null, is_in_range, is_match


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
                            is_func_a(b, explain=True)[0]
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
                            is_func_a(b, explain=True)[0]
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
                            is_func(value, explain=True)[0]
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
        for a in collections:
            is_func_a = is_in(a)
            for b in values:
                with self.subTest('is_in: non-detail == detail'):
                    self.assertEqual(
                        is_func_a(b),
                        is_func_a(b, explain=True)[0]
                    )
                with self.subTest('is_in: {!r}, {!r}'.format(b, a)):
                    self.assertEqual(is_func_a(b), b in a)

    def test_nullability(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, None]
        for name, predicate in [('is_none', is_none), ('is_null', is_null)]:
            for a in values:
                with self.subTest('{}: non-detail == detail'.format(name)):
                    self.assertEqual(
                        predicate(a),
                        predicate(a, explain=True)[0]
                    )
                with self.subTest('{}: {!r}'.format(name, a)):
                    self.assertEqual(predicate(a), a is None)

    def test_patterns(self):
        patterns = [re.compile(r'^\d+$'), r'^[a-z]+$']
        values = ['123', 'abc', 'ABC', '123abc', None, 123]
        for pattern in patterns:
            is_func = is_match(pattern)
            if isinstance(pattern, str):
                pattern = re.compile(pattern)
            for value in values:
                with self.subTest('is_match: non-detail == detail'):
                    self.assertEqual(
                        is_func(value),
                        is_func(value, explain=True)[0]
                    )
                with self.subTest('is_match: {!r}, {!r}'.format(
                    value, pattern.pattern
                )):
                    self.assertEqual(
                        is_func(value),
                        isinstance(value, str) and bool(pattern.match(value))
                    )
