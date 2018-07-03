from unittest import TestCase

from is_valid import Get
from is_valid.test import assert_valid


class TestTest(TestCase):

    def setUp(self):
        self.assertion = assert_valid(True)
        self.assertion_context = assert_valid(Get('a'), context={'a': False})

    def test_pass(self):
        self.assertion(True)

    def test_fail(self):
        with self.assertRaises(AssertionError):
            self.assertion(False)

    def test_fail_with_msg(self):
        with self.assertRaises(AssertionError):
            self.assertion(False, message='foobar')

    def test_pass_context_1(self):
        self.assertion_context(False)

    def test_pass_context_2(self):
        self.assertion_context(True, context={'a': True})

    def test_fail_context_1(self):
        with self.assertRaises(AssertionError):
            self.assertion_context(True)

    def test_fail_context_2(self):
        with self.assertRaises(AssertionError):
            self.assertion_context(False, context={'a': True})
