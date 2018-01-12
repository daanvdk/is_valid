from unittest import TestCase
import json

from is_valid import Explanation


class ExplanationTest(TestCase):

    def setUp(self):
        self.explanation = Explanation(
            True, 'code', 'message', 'details'
        )

    def test_str(self):
        self.assertEqual(str(self.explanation), 'code: message')

    def test_dict(self):
        self.assertEqual(self.explanation.dict(), dict(
            code='code', message='message', details='details',
        ))

    def test_dict_including_valid(self):
        self.assertEqual(self.explanation.dict(include_valid=True), dict(
            valid=True, code='code', message='message', details='details',
        ))

    def test_json(self):
        self.assertEqual(self.explanation.json(), json.dumps(dict(
            code='code', message='message', details='details',
        )))

    def test_dict_advanced(self):
        self.maxDiff = None
        base = dict(valid=True, code='code', message='message')
        explanation = Explanation(
            True, 'code', 'message',
            details=[
                Explanation(**base),
                {'explanation': Explanation(**base)},
                (Explanation(**base),),
            ]
        )
        self.assertEqual(explanation.dict(include_valid=True), dict(
            base, details=[base, {'explanation': base}, (base,)]
        ))
