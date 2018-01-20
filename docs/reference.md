# Index
- [Predicate](#predicate)
- [Explanation](#explanation)
- [is_all](#is_all)
- [is_any](#is_any)
- [is_bool](#is_bool)
- [is_byte](#is_byte)
- [is_cond](#is_cond)
- [is_date](#is_date)
- [is_datetime](#is_datetime)
- [is_dict](#is_dict)
- [is_dict_of](#is_dict_of)
- [is_dict_where](#is_dict_where)
- [is_eq](#is_eq)
- [is_fixed](#is_fixed)
- [is_float](#is_float)
- [is_geq](#is_geq)
- [is_gt](#is_gt)
- [is_if](#is_if)
- [is_in](#is_in)
- [is_in_range](#is_in_range)
- [is_instance](#is_instance)
- [is_int](#is_int)
- [is_iterable](#is_iterable)
- [is_iterable_of](#is_iterable_of)
- [is_iterable_where](#is_iterable_where)
- [is_json](#is_json)
- [is_json_where](#is_json_where)
- [is_leq](#is_leq)
- [is_list](#is_list)
- [is_list_of](#is_list_of)
- [is_list_where](#is_list_where)
- [is_lt](#is_lt)
- [is_match](#is_match)
- [is_none](#is_none)
- [is_not](#is_not)
- [is_nothing](#is_nothing)
- [is_null](#is_null)
- [is_nullable](#is_nullable)
- [is_number](#is_number)
- [is_object_where](#is_object_where)
- [is_one](#is_one)
- [is_optional](#is_optional)
- [is_set](#is_set)
- [is_set_of](#is_set_of)
- [is_something](#is_something)
- [is_str](#is_str)
- [is_subdict_where](#is_subdict_where)
- [is_superdict_where](#is_superdict_where)
- [is_time](#is_time)
- [is_timedelta](#is_timedelta)
- [is_transformed](#is_transformed)
- [is_tuple](#is_tuple)
- [is_tuple_of](#is_tuple_of)
- [is_tuple_where](#is_tuple_where)
- [is_with](#is_with)
- [Get](#Get)
- [test.assert_valid](#testassert_valid)
- [utils.explain](#utilsexplain)
- [utils.Wrapper](#utilswrapper)

# Predicate
The base class of all predicates within this library. It will never get
instantiated directly.

It's instances can be called  as a function with the spec
`(data, explain=False, context={})` where `data` is the data that you want to 
evaluate, explain is whether you want a full [Explanation](#explanation)-object
or just a `bool` value as return value. For now we won't bother about the
context argument, this will further be explained at [is_with](#is_with) and
[Get](#Get).

There is also a convenience function `.explain(data, context={})` that does the
same as the function described above but with `explain=True`.

# Explanation
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

# is_all

# is_any

# is_bool

# is_byte

# is_cond

# is_date

# is_datetime

# is_dict

# is_dict_of

# is_dict_where

# is_eq

# is_fixed

# is_float

# is_geq

# is_gt

# is_if

# is_in

# is_in_range

# is_instance

# is_int

# is_iterable

# is_iterable_of

# is_iterable_where

# is_json

# is_json_where

# is_leq

# is_list

# is_list_of

# is_list_where

# is_lt

# is_match

# is_none

# is_not

# is_nothing

# is_null

# is_nullable

# is_number

# is_object_where

# is_one

# is_optional

# is_set

# is_set_of

# is_something

# is_str

# is_subdict_where

# is_superdict_where

# is_time

# is_timedelta

# is_transformed

# is_tuple

# is_tuple_of

# is_tuple_where

# is_with

# Get

# test.assert_valid

# utils.explain

# utils.Wrapper

