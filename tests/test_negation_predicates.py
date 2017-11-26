from unittest import TestCase

from hypothesis import given
import hypothesis.strategies as hs

from is_valid import is_lt, is_not


class TestNegationPredicates(TestCase):

    @given(hs.floats(), hs.floats())
    def test_not(self, a, b):
        pred = is_lt(a)
        not_pred = is_not(pred)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(not_pred(b), not_pred(b, explain=True).valid)
        with self.subTest('pred correct'):
            self.assertNotEqual(pred(b), not_pred(b))

    @given(hs.floats(), hs.floats())
    def test_not_not(self, a, b):
        pred = is_lt(a)
        not_pred = is_not(is_not(pred))
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(not_pred(b), not_pred(b, explain=True).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(b), not_pred(b))

    @given(
        hs.sampled_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        hs.sampled_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    )
    def test_not_on_non_pred(self, a, b):
        pred = is_not(a)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(b), pred(b, explain=True).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(b), a != b)