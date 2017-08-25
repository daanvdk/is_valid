from unittest import TestCase

from hypothesis import given
import hypothesis.strategies as hs

from is_valid import is_any, is_all, is_one, is_if, is_cond, is_something,\
    is_nothing


class TestConditionPredicates(TestCase):

    @given(hs.lists(hs.sampled_from([
        is_something, is_nothing
    ]), min_size=1, max_size=5))
    def test_is_any(self, preds):
        pred = is_any(*preds)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(1), pred(1, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(pred(1), any(p == is_something for p in preds))

    @given(hs.lists(hs.sampled_from([
        is_something, is_nothing
    ]), min_size=1, max_size=5))
    def test_is_all(self, preds):
        pred = is_all(*preds)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(1), pred(1, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(pred(1), all(p == is_something for p in preds))

    @given(hs.lists(hs.sampled_from([
        is_something, is_nothing
    ]), min_size=1, max_size=5))
    def test_is_one(self, preds):
        pred = is_one(*preds)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(1), pred(1, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(
                pred(1), sum(1 for p in preds if p == is_something) == 1
            )

    @given(
        hs.sampled_from([is_something, is_nothing]),
        hs.sampled_from([is_something, is_nothing])
    )
    def test_is_if(self, cond, pred):
        pred = is_if(cond, pred)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(1), pred(1, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(pred(1), pred(1) if cond(1) else True)

    @given(
        hs.sampled_from([is_something, is_nothing]),
        hs.sampled_from([is_something, is_nothing]),
        hs.sampled_from([is_something, is_nothing])
    )
    def test_is_if_with_else(self, cond, pred_if, pred_else):
        pred = is_if(cond, pred_if, pred_else)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(1), pred(1, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(pred(1), pred_if(1) if cond(1) else pred_else(1))

    @given(hs.lists(hs.tuples(
        hs.sampled_from([is_something, is_nothing]),
        hs.sampled_from([is_something, is_nothing])
    ), min_size=1, max_size=5))
    def test_conds(self, conds):
        pred = is_cond(*conds)
        with self.subTest('explain=True == explain=False'):
            self.assertEqual(pred(1), pred(1, explain=True)[0])
        with self.subTest('pred correct'):
            self.assertEqual(
                pred(1),
                next((pred(1) for cond, pred in conds if cond(1)), False)
            )
