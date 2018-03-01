# Predicate
`Predicate()`

The base class of all predicates within this library. It will never get
instantiated directly.

It's instances can be called  as a function with the spec
`(data, explain=False, context={})` where `data` is the data that you want to 
evaluate, explain is whether you want a full [`Explanation`](#explanation)
object or just a `bool` value as return value. For now we won't bother about
the context argument, this will further be explained at [`is_with`](#is_with)
and [`Get`](#get).

There is also a convenience function `.explain(data, context={})` that does the
same as the function described above but with `explain=True`.

It is also possible to use the `&` and `|` operators on two predicates, these
wrap the two predicates with [`is_all`](#is_all) and [`is_any`](#is_any)
predicate classes respectively.

The `~` operator will wrap a predicate with [`is_not`](#is_not).

# Explanation
`Explanation(valid, code, message, details=None)`

The class of the results that you get when calling a predicate with `.explain`
or `explain=True`.

All explanation have the attributes `valid`, `code`, and `message` that
respectively hold whether the data was valid, a code for the kind of result and
a message that explains the result. A lot of explanation objects also have an
attribute called `details` that gives more in depth explanation about the
result.

The truth value of an explanation objects depends on whether the result was
valid or not.

You can also call `.dict(include_valid=False, include_details=True)` on an
explanation object that will translate the explanation to a data structure
consisting out of basic data types like `dict`. `list` and `str`.

There is also the convenience function
`.json(include_valid=False, include_details=True)` that does the same as
`.dict` but encodes it to json.


# Get
`Get(key)`

An object that when used within predicates as a value will be substituted for
the value corresponding to the given key within the context. If the key is not
present within the context the predicate will automatically fail.

# is_all
`is_all(*predicates)`

Creates a predicate that evaluates if all of the given predicates hold. If
called with explanation it's details arguments will be a `list` of
[`Explanation`](#explanation) objects. If the predicate holds the explanation
of all predicates that held are included, otherwise the explanation of all
predicates that did not hold are included.

# is_any
`is_any()`

Creates a predicate that evaluates if any of the given predicates hold. If
called with explanation it's details arguments will be a `list` of
[`Explanation`](#explanation) objects. If the predicate holds the explanation
of all predicates that held are included, otherwise the explanation of all
predicates that did not hold are included.

# is_bool
`is_bool`

A predicate that checks whether the data is an instance of `bool`.

# is_byte
`is_byte`

A predicate that checks whether the data is an instance of `int` and is higher
or equal to `0` and lower or equal to `255`.

# is_cond
`is_cond(*conditions, cond_trans=identity, pred_trans=identity, default=is_no_match)`

Creates a predicate where conditions are 2-tuples of predicates called the
condition and the predicate, for the first condition to hold the predicate will
be evaluated. If none of the conditions hold the `default` argument will be
used as predicate.

The `cond_trans` and `pred_trans` will let you specify functions that will
transform the data before it is fed to the conditions and predicates
respectively.

# is_date
`is_date`

A predicate that checks whether the data is an instance of `datetime.date`.

# is_datetime
`is_datetime`

A predicate that checks whether the data is an instance of `datetime.datetime`.

# is_dict
`is_dict`

A predicate that checks whether the data is an instance of `dict`.

# is_dict_of
`is_dict_of(key_predicate, value_predicate)`

Creates a predicate that checks if the data is an instance of `dict` where all
the keys are valid according to `key_predicate` and all the values are valid
according to `value_predicate`.

If called with explanations the
[`Explanation`](#explanation) object's details attribute will contain a `dict`
mapping of the keys of entries that were not considered valid according to the
predicates to a `dict` containing a mapping of either `key`, `value` or both to
the corresponding explanation objects. When valid all explanations that were
valid will be included, when invalid all explanations that were invalid will be
included.

# is_dict_where
`is_dict_where(**kwargs)`<br />
`is_dict_where(mapping, **kwargs)`<br />
`is_dict_where(iterable, **kwargs)`<br />
`is_dict_where(required, optional)`

Creates a predicate that checks if the data is an instance of `dict` where the
keys and values follow a certain specification.

The first three ways to instantiate this class are similar to the ways to call
`dict` and will work the same way to provide keys and corresponding predicates.
The predicate will then require the data to consist exactly out of these keys
and have all predicates hold for the corresponding value.

The second way to instantiate this class is a bit different, here you give two
mappings as arguments which then correspond respectively to the required keys
and their corresponding predicates and the optional keys and their
corresponding predicates.

# is_eq
`is_eq(value)`

Creates a predicate that checks if the data is equal to the given value.

# is_fixed
`is_fixed(valid, code, message, details=None)`

Creates a predicate that will always return the exact same explanation
following the provided arguments.

# is_float
`is_float`

A predicate that checks whether the data is an instance of `float`.

# is_geq
`is_geq(value)`

Creates a predicate that checks if the data is greater or equal to the given
value.

# is_gt
`is_gt(value)`

Creates a predicate that checks if the data is greater than the given value.

# is_if
`is_if(condition, if_predicate, else_predicate=None, else_valid=True)`

Creates a predicate that given a predicate as condition will based on the
result of this condition on the data evaluate the data with either
`if_predicate` or `else_predicate`. If the else predicate is omitted it will
use the value of `else_valid` for when the condition considers the data
invalid, as explanation it will reuse the explanation that the condition
returned.

# is_in
`is_in(collection)`

Generates a predicate that checks if the data is within the given collection.

# is_in_range
`is_in_range(start, stop, start_in=True, stop_in=False, start_rep=None, stop_rep=None)`

Generates a predicate that checks if the data is within the range specified
by `start` and `stop`. The optional arguments `start_in` and `stop_in` specify
whether respectively `start` and `stop` should be included or excluded from the
range. The `start_rep` and `stop_rep` arguments will determine what the start
and stop value will be called within the explanations, if no values are
provided `repr(start)` and `repr(stop)` will be used.

# is_instance
`is_instance(cls, rep=None)`

Creates a predicate that checks if the data is an instance of the given class.
You can use the `rep` argument to specify what an instance of this class should
be called. If you don't do this it will default to
`an instance of {cls.__name__}`.

# is_int
`is_int`

A predicate that checks whether the data is an instance of `int`.

# is_iterable
`is_iterable`

A predicate that checks whether the data is iterable.

# is_iterable_of
`is_iterable_of(predicate)`

Creates a predicate that checks that the data is an iterable where every
element of the data is valid according to the given predicate.

If called with explanation the [`Explanation`](#explanation) object's details
attribute will contain a mapping of indexes to the explanation objects
corresponding to the element with that index.

If the predicate holds all explanations will be included, if the predicate does
not hold only the explanations of the elements that did not hold according to
the given predicate will be included.

# is_iterable_where
`is_iterable_where(*predicates)`

Creates a predicate that checks that the data is an iterable where the 1st
element of the data is valid according to the 1st given predicate, the 2nd
element of the data is valid according to the 2nd given predicate and so on.
Also requires that the amount of elements in the iterable is equal to the
amount of predicates given.

If called with explanation the [`Explanation`](#explanation) object's details
attribute will contain a mapping of indexes to the explanation objects
corresponding to the element with that index.

If the predicate holds all explanations will be included, if the predicate does
not hold only the explanations of the elements that did not hold according to
the given predicate will be included.

# is_json
`is_json`

A predicate that checks whether the data is a `str` containing valid json.

# is_json_where
`is_json_where(predicate, loader=json.loads)`

Creates a predicate that checkes whether the data is a `str`, contains valid
json, and the given predicate holds for the decoded json.

With the `loader` parameter you can specify an alternative JSON loader.

# is_leq
`is_leq(value)`

Creates a predicate that checks if the data is lower or equal to the given
value.

# is_list
`is_list`

A predicate that checks whether the data is an instance of `list`.

# is_list_of
`is_list_of()`

Similar to [`is_iterable_of`](#is_iterable_of) but checks if the data is an
instance of `list` as well.

# is_list_where
`is_list_where()`

Similar to [`is_iterable_where`](#is_iterable_where) but checks if the data is
an instance of `list` as well.


# is_lt
`is_lt(value)`

Creates a predicate that checks if the data is lower than the given value.

# is_match
`is_match(regex, flags=0, full=False, rep=None)`
A predicate that checks if the data matches the given pattern. If a string is
provided as a pattern this predicate will compile it first. The optional
parameter `flags` allows you to specify flags for this compilation.

The `full` parameter determines whether the `match` or the `fullmatch` function
will be used to find a match.

The `rep` parameter determines how the pattern will be represented in the
explanation. If no `rep` is provided the pattern itself will be shown.

# is_none
`is_none`

A predicate that checks whether the data is `None`.

# is_not
`is_not(predicate)`

Creates a predicate that is the inverse of the given predicate.

# is_nothing
`is_nothing`

The strongest existing predicate, since data is always something this predicate
will never hold.

# is_null
`is_null`

Same as [`is_none`](#is_none) but uses the word null in it's explanations
instead of None. Useful for when the explanation will be directly outputted to
something like a JSON API for example.

# is_nullable
`is_nullable(predicate)`

Same as [`is_optional`](#is_optional) but uses the word null in it's explanations
instead of None. Useful for when the explanation will be directly outputted to
something like a JSON API for example.

# is_number
`is_number`

A predicate that checks whether the data is an instance of either `int` or
`float`.

# is_object_where
`is_object_where(**kwargs)`<br />
`is_object_where(mapping, **kwargs)`<br />
`is_object_where(iterable, **kwargs)`

Same as [`is_superdict_where`](#is_superdict_where) but on object attributes
instead of mapping keys.

# is_one
`is_one(*predicates)`

Creates a predicate that evaluates if exactly one of the given predicates hold.
If called with explanation it's [`Explanation`](#explanation) object's details
arguments will be the explanation of the one predicate that held if exactly one
predicate holds, if none of the predicates hold it will be a list of all
explanations, if more than one of the predicates hold it will be a list of the
explanations of the predicates that did hold.

# is_optional
`is_optional(predicate)`

Creates a predicate that checks if the data is `None` or holds according to the
given predicate.

# is_set
`is_set`

A predicate that checks whether the data is an instance of `set`.

# is_set_of
`is_set_of()`

Similar to [`is_iterable_of`](#is_iterable_of) but checks if the data is an
instance of `set` as well.

Also since a `set` has no explicit ordering the keys within the explanations
are the elements themselves instead of indexes.

# is_something
`is_something`

The weakest predicate possible, because data is always something this predicate
always holds.

# is_str
`is_str`

A predicate that checks whether the data is an instance of `str`.

# is_subdict_where
`is_subdict_where(**kwargs)`<br />
`is_subdict_where(mapping, **kwargs)`<br />
`is_subdict_where(iterable, **kwargs)`

Similar to [`is_dict_where`](#is_dict_where) but does not care about missing
keys.

# is_superdict_where
`is_superdict_where(**kwargs)`<br />
`is_superdict_where(mapping, **kwargs)`<br />
`is_superdict_where(iterable, **kwargs)`

Similar to [`is_dict_where`](#is_dict_where) but does not care about extra
keys.

# is_time
`is_time`

A predicate that checks whether the data is an instance of `datetime.time`.

# is_timedelta
`is_timedelta`

A predicate that checks whether the data is an instance of
`datetime.timedelta`.

# is_transformed
`is_transformed(transform, success, fail=is_not_transformable, exceptions=[Exception])`

Creates a predicate that checks if the data is valid according to the predicate
provided with the `success` parameter after transforming it with the
`transform` parameter. If one of the errors in the `exceptions` parameter
occurs during this transformation this exception is caught and the `fail`
predicate is used on the data instead.

# is_tuple
`is_tuple`

A predicate that checks whether the data is an instance of `tuple`.

# is_tuple_of
`is_tuple_of(predicate)`

Similar to [`is_iterable_of`](#is_iterable_of) but checks if the data is an
instance of `tuple` as well.

# is_tuple_where
`is_tuple_where()`

Similar to [`is_iterable_where`](#is_iterable_where) but checks if the data is
an instance of `tuple` as well.

# is_with
`is_with(context, success, fail=fail)`

Creates a predicate that given a mapping of keys to functions that transform
data to something else through the `context` parameter, uses these functions to
add context for the corresponding key. The `success` predicate is then called
with this context. If setting the context fails because any of the functions
raises an exception the data is evaluated with the `fail` predicate instead.

# test.assert_valid
`test.assert_valid(predicate)`

Transforms a predicate to a function with spec
`(data, message=None, advanced=True)`, this function does nothing if the data
is valid according to the predicate but throws an `AssertionError` when it is
not valid. You can supply your own custom message through the `message`
parameter. When no message is supplied the [`Explanation`](#explanation) object
is used instead. The `advanced` parameter determines if this object is
transformed into a string with `repr` or `str`, where `repr` is advanced.

# utils.explain
`utils.explain(predicate, code='valid', message_valid='Data is valid', message_invalid='Data is not valid', details_valid=None, details_invalid=None)`

Wraps a function that returns a `bool` for some data to act like any of the
other predicates in this library.

The `code`, `message_valid`, `message_invalid`, `details_valid`, and
`details_invalid` arguments then specify what the [`Explanation`](#explanation)
objects returned by this value will look like.

# utils.Wrapper
`utils.Wrapper(wrapped=None)`

Wraps a predicate within an object that also acts like a predicate. The wrapped
predicate can easily be changed by calling `.wrap(predicate)` on the object to
set a new predicate to wrap.

This is useful to fix cyclic dependencies within predicates.
