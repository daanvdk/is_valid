from unittest import TestCase

from is_valid import is_anything, is_nothing


class TestExtremePredicates(TestCase):

    def test_extremes(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, None]
        for name, validator, expected in [
            ('is_anything', is_anything, True),
            ('is_nothing', is_nothing, False),
        ]:
            for a in values:
                with self.subTest('{}: non-detail == detail'.format(name)):
                    self.assertEqual(
                        validator(a),
                        validator(a, detailed=True)[0]
                    )
                with self.subTest('{}: {!r}'.format(name, a)):
                    self.assertEqual(validator(a), expected)
