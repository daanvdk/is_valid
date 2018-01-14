from unittest import TestCase

from hypothesis import given

from is_valid import is_something, is_nothing
from is_valid.base import Predicate

from .utils import varying


class TestExtremePredicates(TestCase):

    @given(varying)
    def test_something(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_something(value), is_something.explain(value).valid
            )
        with self.subTest('pred correct'):
            self.assertTrue(is_something(value))

    @given(varying)
    def test_nothing(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_nothing(value), is_nothing.explain(value).valid
            )
        with self.subTest('pred correct'):
            self.assertFalse(is_nothing(value))

    def test_predicate(self):
        predicate = Predicate()
        with self.assertRaises(NotImplementedError):
            predicate(0)
        with self.assertRaises(NotImplementedError):
            predicate.explain(0)
