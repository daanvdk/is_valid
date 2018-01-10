from unittest import TestCase

from is_valid import is_eq, is_something, is_nothing
from is_valid.utils import explain, PredicateWrapper


class TestExplain(TestCase):

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


class TestPredicateWrapper(TestCase):

    def test_wrapper_predicate(self):
        wrapper = PredicateWrapper()
        with self.assertRaises(AttributeError):
            wrapper(None)
        wrapper.predicate = is_something
        self._test(wrapper, None, True)
        wrapper.predicate = is_nothing
        self._test(wrapper, None, False)

    def test_wrapper_predicate_with_arg(self):
        wrapper = PredicateWrapper(is_something)
        self._test(wrapper, None, True)
        wrapper.predicate = is_nothing
        self._test(wrapper, None, False)
    
    def _test(self, predicate, value, expected):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                predicate(value),
                predicate(value, explain=True).valid
            )
        with self.subTest('pred correct'):
            self.assertEqual(predicate(value), expected)
