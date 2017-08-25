from unittest import TestCase

from is_valid import is_something, is_nothing


class TestExtremePredicates(TestCase):

    def test_extremes(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, None]
        for name, predicate, expected in [
            ('is_something', is_something, True),
            ('is_nothing', is_nothing, False),
        ]:
            for a in values:
                with self.subTest('{}: non-detail == detail'.format(name)):
                    self.assertEqual(
                        predicate(a),
                        predicate(a, explain=True)[0]
                    )
                with self.subTest('{}: {!r}'.format(name, a)):
                    self.assertEqual(predicate(a), expected)
