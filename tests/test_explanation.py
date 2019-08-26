from unittest import TestCase
import json

from is_valid import Explanation


class ExplanationTest(TestCase):

    def setUp(self):
        self.explanation = Explanation(
            True, 'code', 'message', 'details'
        )

    def test_summary(self):
        self.assertEqual(str(self.explanation), 'message')

    def test_dict(self):
        self.assertEqual(self.explanation.dict(), dict(
            code='code', message='message', details='details',
        ))

    def test_dict_including_valid(self):
        self.assertEqual(self.explanation.dict(include_valid=True), dict(
            valid=True, code='code', message='message', details='details',
        ))

    def test_json(self):
        self.assertEqual(json.loads(self.explanation.json()), dict(
            code='code', message='message', details='details',
        ))

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


class ExplanationMergeTest(TestCase):

    def test_merge_all_not_valid(self):
        foo = Explanation(False, 'foo', '')
        bar = Explanation(False, 'bar', '')
        merged = foo + bar

        self.assertEqual(merged.valid, False)
        self.assertEqual(merged.code, 'not_all_hold')
        self.assertEqual(merged.details, [foo, bar])

    def test_merge_all_valid(self):
        foo = Explanation(True, 'foo', '')
        bar = Explanation(True, 'bar', '')
        merged = foo + bar

        self.assertEqual(merged.valid, True)
        self.assertEqual(merged.code, 'all_hold')
        self.assertEqual(merged.details, [foo, bar])

    def test_merge_some_not_valid(self):
        foo = Explanation(True, 'foo', '')
        bar = Explanation(False, 'bar', '')
        merged = foo + bar

        self.assertEqual(merged, bar)

    def test_merge_dict(self):
        foo = Explanation(False, 'not_dict_where', '', {
            'foo': Explanation(False, 'foo', 'foo')
        })
        bar = Explanation(False, 'not_dict_where', '', {
            'bar': Explanation(False, 'bar', 'bar'),
        })
        merged = foo + bar

        self.assertEqual(merged.valid, False)
        self.assertEqual(merged.code, 'not_dict_where')
        self.assertEqual(merged.details, {
            'foo': foo.details['foo'],
            'bar': bar.details['bar'],
        })
