from unittest import TestCase

from is_valid import is_eq
from is_valid.test import IsValidMixin

from .utils import MockTestCase


class MockTest(MockTestCase, IsValidMixin):

    def test_pass(self):
        self.assertIsValid(is_eq(True), True)

    def test_fail(self):
        self.assertIsValid(is_eq(True), False)

    def test_fail_with_msg(self):
        self.assertIsValid(is_eq(True), False, msg='foobar')


class TestTest(TestCase):

    def test_test(self):
        mocktest = MockTest()
        mocktest.run()
        with self.subTest('pass'):
            passed, e = mocktest.results['test_pass']
            self.assertTrue(passed)
        with self.subTest('fail'):
            passed, e = mocktest.results['test_fail']
            self.assertFalse(passed)
        with self.subTest('fail_with_msg'):
            passed, e = mocktest.results['test_fail_with_msg']
            self.assertFalse(passed)
            self.assertEqual(str(e), 'foobar')
