from unittest import TestCase

from hypothesis import given

from is_valid import is_something, is_nothing

from .utils import varying


class TestExtremePredicates(TestCase):

    @given(varying)
    def test_something(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_something(value), is_something(value, explain=True).valid
            )
        with self.subTest('pred correct'):
            self.assertTrue(is_something(value))

    @given(varying)
    def test_nothing(self, value):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                is_nothing(value), is_nothing(value, explain=True).valid
            )
        with self.subTest('pred correct'):
            self.assertFalse(is_nothing(value))
