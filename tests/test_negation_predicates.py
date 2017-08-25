from unittest import TestCase

from is_valid import is_not, is_eq, is_neq


class TestNegationPredicates(TestCase):

    def setUp(self):
        self.values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_negation(self):
        for a in self.values:
            for name, func_a, not_func_a, eq in [
                ('is_eq__not_is_eq',
                    is_eq(a), is_not(is_eq(a)), False),
                ('is_eq__not_is_neq',
                    is_eq(a), is_not(is_neq(a)), True),
                ('is_neq__not_is_eq',
                    is_neq(a), is_not(is_eq(a)), True),
                ('is_neq__not_is_neq',
                    is_neq(a), is_not(is_neq(a)), False),
                ('is_eq__not_not_is_eq',
                    is_eq(a), is_not(is_not(is_eq(a))), True),
                ('is_eq__not_not_is_neq',
                    is_eq(a), is_not(is_not(is_neq(a))), False),
                ('is_neq__not_not_is_eq',
                    is_neq(a), is_not(is_not(is_eq(a))), False),
                ('is_neq__not_not_is_neq',
                    is_neq(a), is_not(is_not(is_neq(a))), True),
            ]:
                for b in self.values:
                    with self.subTest(
                        'explain == no-explain, {} {} {}'.format(name, a, b)
                    ):
                        self.assertEqual(
                            not_func_a(a), not_func_a(a, explain=True)[0]
                        )
                    with self.subTest('{} {} {}'.format(name, a, b)):
                        self.assertEqual(func_a(b) == eq, not_func_a(b))
