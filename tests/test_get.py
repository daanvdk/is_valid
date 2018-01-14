from unittest import TestCase
from is_valid import is_with, is_dict_where, is_list_of, is_str, is_number,\
    is_transformed, Get


class TestGet(TestCase):

    def setUp(self):
        self.pred = is_with(
            'len', lambda data: len(data['columns']),
            is_dict_where(
                columns=is_list_of(is_str),
                rows=is_list_of(
                    is_list_of(is_number) &
                    is_transformed(len, Get('len'))
                )
            ),
        )

    def test_correct(self):
        value = {
            'columns': ['A', 'B', 'C'],
            'rows': [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
            ],
        }
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                self.pred(value),
                self.pred.explain(value).valid
            )
        with self.subTest('pred correct'):
            self.assertEqual(self.pred(value), True)

    def test_value_error(self):
        value = {
            'colums': ['A', 'B', 'C'],
            'rows': [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
            ],
        }
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                self.pred(value),
                self.pred.explain(value).valid
            )
        with self.subTest('pred correct'):
            self.assertEqual(self.pred(value), False)

    def test_incorrect_key(self):
        value = {
            'columns': ['A', 'B', 'C'],
            'rows': [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
            ],
        }
        pred = is_with(
            'len', lambda data: len(data['columns']),
            is_dict_where(
                columns=is_list_of(is_str),
                rows=is_list_of(
                    is_list_of(is_number) &
                    is_transformed(len, Get('length'))
                )
            ),
        )
        with self.subTest('explain=True'):
            with self.assertRaises(ValueError):
                pred.explain(value)
        with self.subTest('explain=False'):
            with self.assertRaises(ValueError):
                pred(value)
