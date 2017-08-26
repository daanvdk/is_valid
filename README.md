<h1 align="center">
    <img src="https://raw.githubusercontent.com/Daanvdk/is_valid/master/logo.png" /><br />
    Is Valid?
</h1>

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
Predicates are functions that given a certain input return either `True` or
`False` according to some rules that the input either follows or does not
follow.

## Example
We are going to write a predicate that validates that our data is a list of
books.
```python
is_list_of_books = is_list_of(
    is_dict_where(
        title=is_str,
        author=is_str,
        pubdate=is_date,
        ISBN=is_match(r'^\d{9}(\d|X)$')
    )
)
```
You can see that using only a few simple predicates you can easily create a
predicate that evaluates complex structures of data.

However sometimes just `True` or `False` doesn't cut it, you might want to know
why your data is valid or not. For this purpose all predicates include an
optional argument `explain`. If you pass `explain=True` with the predicate you
will get a 2-tuple `(valid, explanation)` as result.

We will show you this using the following data:
```python
books = [
    {
        'title': 'A Game of Thrones',
        'author': 'George R. R. Martin',
        'pubdate': datetime.date(1996, 8, 1),
        'ISBN': '0553103547'
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'pubdate': '1997-6-26',
        'ISBN': '0747532699'
    },
    {
        'title': 'The Fellowship of the Ring',
        'author': 'J. R. R. Tolkien',
        'pubdate': datetime.date(1954, 7, 29),
        'ISBN': '0-618-57494-8'
    }
]
```
If we call our predicate `is_list_of_books` on this data with the
`explain=True` option we get the following result:
```python
(False, {
    1: {'pubdate': 'data is not a datetime'},
    2: {'ISBN': 'data does not match /^\d{9}(\d|X)$/'}
})
```
We can then exactly see what is wrong, and with which book.


## Installation
'Is Valid?' is on [PyPI](https://pypi.python.org/pypi/is-valid), you can install it with:
```
pip install is-valid
```
The module is written in pure python without any dependencies and is only a few
hundred LOC.
