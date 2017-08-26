# ![](https://raw.githubusercontent.com/Daanvdk/is_valid/master/logo.png) Is Valid?
[![pypi_version](
    https://badge.fury.io/py/is-valid.svg
)](https://pypi.python.org/pypi/is-valid)
[![build_status](
    https://travis-ci.org/Daanvdk/is_valid.svg?branch=master
)](https://travis-ci.org/Daanvdk/is_valid)
[![code_coverage](
    https://codecov.io/gh/Daanvdk/is_valid/branch/master/graph/badge.svg
)](https://codecov.io/gh/Daanvdk/is_valid)

'Is Valid?' is a simple lightweight python library for validation predicates.

## Usage
There are a lot of very basic predicates like `is_str`:
```python
>>> is_str("foobar")
True
>>> is_str(None)
False
```
But also more complex predicate generators like `is_match` or `is_list_of`:
```python
>>> is_integer_string = is_match(r'^\d+$')
>>> is_integer_string('12345')
True
>>> is_integer_string('12A45')
False
>>> is_list_of_integer_strings = is_list_of(is_integer_string)
>>> is_list_of_integer_strings(['123', '456', '789'])
True
>>> is_list_of_integer_strings(['123', 'ABC', '789'])
False
>>> is_list_of_integer_strings({'123', '456', '789'})
False
```
As you can see in the example above by nesting predicates you can create very
powerful predicates that evaluate complex structures easily.

In some cases just `True` or `False` doesn't cut it, you might want to know why
this is the case. For this purpose all predicates take an `explain` keyword
argument.
```python
>>> is_str("foobar", explain=True)
(True, 'data is a str')
>>> is_str(None, explain=True)
(False, 'data is not a str')
>>> is_integer_string('12345', explain=True)
(True, 'data does match /^\d+$/')
>>> is_integer_string('12A45', explain=True)
(False, 'data does not match /^\d+$/')
>>> is_list_of_integer_strings(['123', '456', '789'], explain=True)
(True, {
     0: 'data does match /^\d+$/',
     1: 'data does match /^\d+$/',
     2: 'data does match /^\d+$/'
})
>>> is_list_of_integer_strings(['123', 'ABC', '789'], explain=True)
(False, {1: 'data does not match /^\d+$/'})
>>> is_list_of_integer_strings({'123', '456', '789'}, explain=True)
(False, 'data is not an instance of list')
```
You can also use this module for unittests, the module provides a mixin called
`IsValidMixin` that you can mix in with your `TestCase` class to have access to
`self.assertIsValid(predicate, data, msg=None)` in your tests. If you don't
provide a message the message of your assert error will be the error that the
predicate gives when `explain=True`.

# Install
'Is Valid?' is on [PyPI](https://pypi.python.org/pypi/is-valid), you can install it with:
```
pip install is-valid
```
The module is written in pure python without any dependencies and is only a few
hundred LOC.
