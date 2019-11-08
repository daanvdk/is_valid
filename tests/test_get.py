from unittest import TestCase
from is_valid import is_with, is_dict_where, is_list_of, is_str, is_number,\
    is_transformed, Get, is_eq


class TestTablePred(TestCase):

    def setUp(self):
        self.pred = is_with(
            {'len': lambda data: len(data['columns'])},
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
            {'len': lambda data: len(data['columns'])},
            is_dict_where(
                columns=is_list_of(is_str),
                rows=is_list_of(
                    is_list_of(is_number) &
                    is_transformed(len, Get('length'))
                )
            ),
        )
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(
                pred(value),
                pred.explain(value).valid
            )
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), False)


class TestParam(TestCase):

    def test_correct(self):
        pred = is_eq(Get('a'))
        for context, value, expected in [
            ({'a': 0}, 0, True),
            ({'a': 0}, 1, False),
            ({'a': 1}, 0, False),
            ({'a': 1}, 1, True),
            ({'b': 1}, 1, False),
            ({}, 1, False),
        ]:
            with self.subTest(
                'explain=True == explain=False; {}; {}; {}'
                .format(context, value, expected)
            ):
                self.assertEqual(
                    pred(value, context=context),
                    pred.explain(value, context).valid
                )
            with self.subTest(
                'pred correct; {}; {}; {}'
                .format(context, value, expected)
            ):
                self.assertEqual(pred(value, context=context), expected)
