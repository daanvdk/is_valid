# Is Valid?
'Is Valid?' is a simple lightweight python library to create validation functions
that check that data is in a certain format.

## Usage
There are a lot of very basic functions like `is_str`:
```python
>>> is_str("foobar")
True
>>> is_str(None)
False
```
But also more complex functions like `is_match` or `is_list_of`:
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
As you can see in the example above you can nest these functions very easily
creating powerful validation functions that examine complex structures easily.

In some cases just `True` or `False` doesn't cut it, you might want to know why
your data is invalid. For this purpose all validation functions take a
`detailed` keyword argument.
```python
>>> is_str("foobar", detailed=True)
(True, None)
>>> is_str(None, detailed=True)
(False, 'data is not an instance of str')
>>> is_integer_string('12A45', detailed=True)
(False, 'data does not match /^\d+$/')
>>> is_list_of_integer_strings(['123', 'ABC', '789'], detailed=True)
(False, {1: 'data does not match /^\d+$/'})
>>> is_list_of_integer_strings({'123', '456', '789'}, detailed=True)
(False, 'data is not an instance of list')
```
You can also use this module for unittests, the module provides a mixin called
`IsValidMixin` that you can mix in with your `TestCase` class to have access to
`self.assertIsValid(validator, data, msg=None)` in your tests. If you don't
provide a message the message of your assert error will automatically be the
error that the validator gives when `detailed=True`.

# Install
'Is Valid?' is on PyPi, you can install it with:
```
pip install isvalid
```
The module is written in pure python without any dependencies and is only a few
hundred LOC.
