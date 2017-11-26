from unittest import TestCase

from is_valid import is_eq
from is_valid.utils import explain


class TestUtils(TestCase):

    def setUp(self):
        self.predicate = explain(is_eq(1), 'valid', 'foo', 'bar')

    def test_explain_valid(self):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                self.predicate(1), self.predicate(1, explain=True).valid
            )
        with self.subTest('pred correct'):
            self.assertEqual(
                self.predicate(1, explain=True).dict(include_valid=True),
                {'valid': True, 'code': 'valid', 'message': 'foo'}
            )

    def test_explain_invalid(self):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                self.predicate(0), self.predicate(0, explain=True).valid
            )
        with self.subTest('pred correct'):
            self.assertEqual(
                self.predicate(0, explain=True).dict(include_valid=True),
                {'valid': False, 'code': 'not_valid', 'message': 'bar'}
            )
