from itertools import combinations
from unittest import TestCase

from hypothesis import given
import hypothesis.strategies as hs

from is_valid import is_eq, is_iterable_where, is_iterable_of, is_dict_where,\
    is_subdict_where, is_superdict_where, is_object_where, is_list_where,\
    is_list_of, is_tuple_where, is_tuple_of, is_set_of, is_int, is_dict_of,\
    is_dict_union

from .utils import dicts, correct_dict, lists, correct_list, tuples,\
    correct_tuple, objects


class TestStructurePredicates(TestCase):

    @given(dicts)
    def test_is_dict_where(self, value):
        pred = is_dict_where(foo=is_eq(True), bar=is_eq(False))
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), value == correct_dict)

    @given(dicts)
    def test_is_dict_where_required_and_optional(self, value):
        pred = is_dict_where(dict(foo=True), dict(bar=True))
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(
                pred(value),
                isinstance(value, dict) and
                value.get('foo', False) and
                value.get('bar', True) and
                'baz' not in value
            )

    @given(dicts)
    def test_is_subdict_where(self, value):
        pred = is_subdict_where(foo=is_eq(True), bar=is_eq(False))
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), isinstance(value, dict) and all(
                key in correct_dict and val == correct_dict[key]
                for key, val in value.items()
            ))

    @given(dicts)
    def test_is_superdict_where(self, value):
        pred = is_superdict_where(foo=is_eq(True), bar=is_eq(False))
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), isinstance(value, dict) and all(
                key in value and val == value[key]
                for key, val in correct_dict.items()
            ))

    @given(hs.dictionaries(
        hs.one_of(hs.integers(), hs.text()),
        hs.one_of(hs.integers(), hs.text()),
        max_size=5
    ))
    def test_is_dict_of(self, value):
        pred = is_dict_of(is_int, is_int)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), isinstance(value, dict) and all(
                isinstance(key, int) and isinstance(val, int)
                for key, val in value.items()
            ))

    @given(hs.dictionaries(
        hs.sampled_from([1, 2]),
        hs.sampled_from([1, 2]),
        max_size=5
    ))
    def test_is_dict_of_on_non_pred(self, value):
        pred = is_dict_of(1, 1)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), isinstance(value, dict) and all(
                entry == (1, 1) for entry in value.items()
            ))

    @given(objects)
    def test_is_object_where(self, value):
        pred = is_object_where(foo=is_eq(True), bar=is_eq(False))
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), (
                isinstance(value, object) and
                getattr(value, 'foo', False) and
                not getattr(value, 'bar', True)
            ))

    @given(lists)
    def test_is_list_where(self, value):
        pred = is_list_where(is_eq(True), is_eq(False))
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), value == correct_list)

    @given(lists)
    def test_is_list_of(self, value):
        pred = is_list_of(is_eq(True))
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(
                pred(value), isinstance(value, list) and all(value)
            )

    @given(tuples())
    def test_is_tuple_where(self, value):
        pred = is_tuple_where(is_eq(True), is_eq(False))
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(pred(value), value == correct_tuple)

    @given(tuples())
    def test_is_tuple_of(self, value):
        pred = is_tuple_of(is_eq(True))
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(
                pred(value), isinstance(value, tuple) and all(value)
            )

    @given(hs.one_of(lists, tuples()))
    def test_is_iterable_where(self, value):
        pred = is_iterable_where(is_eq(True), is_eq(False))
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(
                pred(value), value in (correct_tuple, correct_list)
            )

    @given(hs.one_of(lists, tuples()))
    def test_is_iterable_of(self, value):
        pred = is_iterable_of(True)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(
                pred(value), isinstance(value, (list, tuple)) and all(value)
            )

    @given(hs.one_of(hs.sets(hs.booleans(), max_size=5), hs.booleans()))
    def test_is_set_of(self, value):
        pred = is_set_of(is_eq(True))
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            self.assertEqual(
                pred(value), isinstance(value, set) and all(value)
            )

    @given(hs.one_of(
        *(
            hs.fixed_dictionaries({
                'type': hs.one_of(
                    hs.just('foo'),
                    hs.just('bar'),
                    hs.just('baz'),
                    hs.just('foobar'),
                ),
                **{
                    key: hs.one_of(hs.integers(), hs.text())
                    for key in keys
                },
            })
            for n in range(4)
            for keys in combinations(['foo', 'bar', 'baz'], n)
        ),
        dicts,
        hs.booleans(),
    ))
    def test_is_dict_union(self, value):
        pred = is_dict_union(
            'type',
            foo={'foo': is_int},
            bar={'bar': is_int},
            foobar={'foo': is_int, 'bar': is_int},
        )

        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(value), pred.explain(value).valid)
        with self.subTest('pred correct'):
            if isinstance(value, dict) and 'type' in value:
                if value['type'] == 'foo':
                    valid = (
                        set(value) == {'type', 'foo'} and
                        isinstance(value['foo'], int)
                    )
                elif value['type'] == 'bar':
                    valid = (
                        set(value) == {'type', 'bar'} and
                        isinstance(value['bar'], int)
                    )
                elif value['type'] == 'foobar':
                    valid = (
                        set(value) == {'type', 'foo', 'bar'} and
                        isinstance(value['foo'], int) and
                        isinstance(value['bar'], int)
                    )
                else:
                    valid = False
            else:
                valid = False
            self.assertEqual(pred(value), valid)
