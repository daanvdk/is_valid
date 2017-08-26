from unittest import TestCase
from json import loads

from is_valid import is_json, is_dict_where, is_list_of, is_bool, is_str,\
    is_int

from .utils import json_data, incorrect_json_data, invalid_json_data


class TestWrapperPredicates(TestCase):

    def setUp(self):
        self.pred = is_dict_where(
            foo=is_list_of(
                is_dict_where(
                    bar=is_bool,
                    baz=is_str
                )
            ),
            bar=is_int
        )
        self.json_pred = is_json(self.pred)

    def test_is_json(self):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                self.json_pred(json_data),
                self.json_pred(json_data, explain=True)[0]
            )
        with self.subTest('pred correct'):
            self.assertTrue(self.json_pred(json_data))

    def test_is_json_include(self):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                self.json_pred(json_data),
                self.json_pred(json_data, explain=True)[0]
            )
        with self.subTest('pred correct'):
            valid, data = self.json_pred(json_data, include=True)
            self.assertTrue(valid)
            self.assertEqual(data, loads(json_data))

    def test_is_json_incorrect(self):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                self.json_pred(incorrect_json_data),
                self.json_pred(incorrect_json_data, explain=True)[0]
            )
        with self.subTest('pred correct'):
            self.assertFalse(self.json_pred(incorrect_json_data))

    def test_is_json_invalid(self):
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                self.json_pred(invalid_json_data),
                self.json_pred(invalid_json_data, explain=True)[0]
            )
        with self.subTest('pred correct'):
            self.assertFalse(self.json_pred(invalid_json_data))

    def test_is_json_failing_loader(self):
        def failing_loader(body):
            raise ValueError()

        json_pred = is_json(self.pred, loader=failing_loader)
        with self.subTest('pred raises'):
            with self.assertRaises(ValueError):
                json_pred(json_data)
