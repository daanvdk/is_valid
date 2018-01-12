# Changelog

## [0.5.1](https://pypi.python.org/pypi/is-valid/0.5.0) - 2018/12/12
- Fix bug where `is_dict_of` didn't check if the value was a dict beforehand
but only if it was iterable, thus leading to an exception being thrown when a
value was evaluated that was iterable but not a dict.

## [0.5.0](https://pypi.python.org/pypi/is-valid/0.5.0) - 2018/12/12
- Introduction of this changelog.
- `is_dict_where` now also accepts two dicts as arguments to indicate
required and optional keys respectively.
- The `dict` method on `Explanation` objects now has an extra keyword argument
`include_details=True` to specify if you want it to put the details in the
dict. Also if the details are some kind of structure made up out of dicts,
lists and tuples it now traverses these structures to also convert all
`Explanation` objects within them to dicts. (Small breaking change)
- `Wrapper` utility class introduced, this just wraps a function that you can
change at any moment by setting the `func`-attribute. Useful for when you want
some kind of recursion in your predicate structure.
- Predicate classes `is_optional` and `is_nullable` were added, given a
predicate they become a predicate that holds when either the given predicate
holds or the value is `None`. There are two versions because `is_optional` and
`is_nullable` use `is_none` and `is_null` under the hood respectively.
- `is_cond` now wraps its conds and preds with `is_eq` when they are not
callable. Consistency :)
- Almost complete rewrite without breaking any compatibility making all
predicates be instances of a subclass of `is_valid.base.Predicate` instead of
loose functions. This allows for some neat small things:
    - You can now use `~pred` instead of `is_not(pred)`, also
    `is_not(is_not(pred))` just gives back `pred` now.
    - You can now use `pred1 | pred2` instead of `is_any(pred1, pred2)`, also
    `is_any(pred1, is_any(pred2, pred3))` does the same as
    `is_any(pred1, pred2, pred3)` now.
    - You can now use `pred1 & pred2` instead of `is_all(pred1, pred2)`, also
    `is_all(pred1, is_all(pred2, pred3))` does the same as
    `is_all(pred1, pred2, pred3)` now.
    - You can now use `pred.explain(value)` instead of
    `pred(value, explain=True)`.

## [0.4.0](https://pypi.python.org/pypi/is-valid/0.4.0) - 2017/11/26
- Latest version before introduction of this changelog.