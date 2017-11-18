from unittest import TestCase

from is_valid import is_eq
from is_valid.test import assert_valid

from .utils import MockTestCase


class MockTest(MockTestCase):

    def __init__(self):
        super().__init__()
        self.assertion = assert_valid(True)

    def test_pass(self):
        self.assertion(True)

    def test_fail(self):
        self.assertion(False)

    def test_fail_with_msg(self):
        self.assertion(False, msg='foobar')


class TestTest(TestCase):

    def setUp(self):
        self.mocktest = MockTest()
        self.mocktest.run()

    def test_pass(self):
        passed, e = self.mocktest.results['test_pass']
        self.assertTrue(passed)

    def test_fail(self):
        passed, e = self.mocktest.results['test_fail']
        self.assertFalse(passed)

    def test_fail_with_msg(self):
        passed, e = self.mocktest.results['test_fail_with_msg']
        self.assertFalse(passed)
        self.assertEqual(str(e), 'foobar')
