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
            self.assertEqual(not_pred(b), not_pred(b, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertNotEqual(pred(b), not_pred(b))

    @given(hs.floats(), hs.floats())
    def test_not_not(self, a, b):
        pred = is_lt(a)
        not_pred = is_not(is_not(pred))
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(not_pred(b), not_pred(b, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(pred(b), not_pred(b))
