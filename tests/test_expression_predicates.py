from unittest import TestCase
from is_valid import is_eq, is_neq, is_lt, is_leq, is_gt, is_geq, is_in,\
    is_not_in, is_none, is_not_none


class TestExpressionPredicates(TestCase):

    def test_equivalence(self):
        values = [1, 2, 3, '1', '2', '3', [1, 2, 3], ['1', '2', '3']]
        for name, validator, func in [
            ('is_eq', is_eq, lambda a, b: b == a),
            ('is_neq', is_neq, lambda a, b: b != a),
        ]:
            for a in values:
                is_func_a = validator(a)
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
        for name, validator, func in [
            ('is_lt', is_lt, lambda a, b: b < a),
            ('is_leq', is_leq, lambda a, b: b <= a),
            ('is_gt', is_gt, lambda a, b: b > a),
            ('is_geq', is_geq, lambda a, b: b >= a),
        ]:
            for a in values:
                is_func_a = validator(a)
                for b in values:
                    with self.subTest('{}: non-detail == detail'.format(name)):
                        self.assertEqual(
                            is_func_a(b),
                            is_func_a(b, detailed=True)[0]
                        )
                    with self.subTest('{}: {!r}, {!r}'.format(name, b, a)):
                        self.assertEqual(is_func_a(b), func(a, b))

    def test_collection(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        collections = [set([1, 2, 3]), set([4, 5, 6]), set([7, 8, 9])]
        for name, validator, func in [
            ('is_in', is_in, lambda a, b: b in a),
            ('is_not_in', is_not_in, lambda a, b: b not in a),
        ]:
            for a in collections:
                is_func_a = validator(a)
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
        for name, validator, func in [
            ('is_none', is_none, lambda a: a is None),
            ('is_not_none', is_not_none, lambda a: a is not None),
        ]:
            for a in values:
                with self.subTest('{}: non-detail == detail'.format(name)):
                    self.assertEqual(
                        validator(a),
                        validator(a, detailed=True)[0]
                    )
                with self.subTest('{}: {!r}'.format(name, a)):
                    self.assertEqual(validator(a), func(a))
