from unittest import TestCase

from is_valid import is_something, is_nothing, is_eq
from is_valid.utils import explain, Wrapper


class TestExplain(TestCase):

    def setUp(self):
        self.predicate = explain(1, 'valid', 'foo', 'bar')

    def test_explain_valid(self):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                self.predicate(1), self.predicate.explain(1).valid
            )
        with self.subTest('pred correct'):
            self.assertEqual(
                self.predicate.explain(1).dict(include_valid=True),
                {
                    'valid': True,
                    'code': 'valid',
                    'message': 'foo',
                    'data': 1,
                },
            )

    def test_explain_invalid(self):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                self.predicate(0), self.predicate.explain(0).valid
            )
        with self.subTest('pred correct'):
            self.assertEqual(
                self.predicate.explain(0).dict(include_valid=True),
                {
                    'valid': False,
                    'code': 'not_valid',
                    'message': 'bar',
                    'data': 0,
                },
            )


class TestWrapper(TestCase):

    def test_wrapper_predicate(self):
        wrapper = Wrapper()
        with self.assertRaises(TypeError):
            wrapper(None)
        wrapper.wrap(is_eq(0))
        self._test(wrapper, 0, True)
        wrapper.wrap(is_eq(1))
        self._test(wrapper, 0, False)

    def test_wrapper_predicate_with_arg(self):
        wrapper = Wrapper(is_something)
        self._test(wrapper, None, True)
        wrapper.wrap(is_nothing)
        self._test(wrapper, None, False)

    def _test(self, predicate, value, expected):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                predicate(value),
                predicate.explain(value).valid
            )
        with self.subTest('pred correct'):
            self.assertEqual(predicate(value), expected)
