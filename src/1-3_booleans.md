# 1-3: Booleans

<iframe style="width: 800px;height: 500px" src="https://www.youtube.com/embed/QBD5H64JNQs?si=nwmlmVszwi4GuIQB" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

**Related Notebook:** `1-3_booleans.ipynb`

Our next data type is simple, but crucial. The `bool` type represents boolean values: either `True` or `False`.

> [!NOTE]
> Boolean values are named for [George Boole](https://en.wikipedia.org/wiki/George_Boole), a 19th-century English logician who pioneered logic through binary values. 

## `True` and `False`

The two variants of type `bool` are `True` and `False`. The capitals matter; those specific words are reserved for the `bool` variants. You can see this in action yourself by running the following expressions.

```python
type(True)
# => bool
type(true)
# => NameError: name 'true' is not defined
```

## Expressions and Comparisons

Most of the time, we don't explicitly write out `bool` variants. Instead, we derive these values from **expressions** that evaluate to either `True` or `False`. An expression is any syntactically complete statement in Python that evaluates to a single value. `5` is a valid Python expression, but it does not evaluate to `True` or `False`. We need to test for truth or falsity.

**Comparisons** are a common way to perform such tests (but not the only way, as we'll see later). Comparisons take two values, apply a test, and evaluate to `True` or `False`. You're familiar with this even if you've never written a line of code. Here are the comparison operators in Python

- `==`: Equivalence (i.e. `a` is equivalent to `b`)
- `!=`: Not equivalent
- `>`: Greater than
- `<`: Less than
- `>=`: Greater than *or* equal to
- `<=`: Less than or equal to

In practice this looks like:

```python
7 > 5
# => True
2 <= 3
# => False
2 == 2.0
# => True
2 != 2
# => False
```

### Negation

You see that `!=` is the negation of the equivalence comparison. In some languages, `!` is used to negate *any* boolean expression. In Python, we use the `not` keyword. Go ahead—put `not` in front of any of the comparisons you tried above. `not` flips the value.

## Boolean Operators

Comparisons are useful, but we often need to evaluate more than one boolean expression at a time. Or we need to combine them for a different effect. That's where the `and` and `or` operators come in.

These allow us to combine boolean expressions. For example, `True or False` evaluates to `True`. `True and False` will be `False`.

Just like in mathematical expressions, parentheses matter and affect order of operations. Try these two:

```python
True and not False or True
# => True
True and not (False or True)
# => False
```

## `None`

There is another data type closely related to `bool` known as `NoneType`, with a single value of `None`.

```python
type(None)
# => NoneType
```

This is Python's way of saying "Nothing's here." Other languages use `null` or `nil` to express this concept. I mention it here because `None` is "falsy," meaning that it *kinda* evaluates as false. But only kinda.

```python
None == False
# => False
```

`None` is not *equivalent* to `False`. But given an `or` statement between `None` and another value:

```python
None or 10
# => 10
```

You'll get the non-`None` value.

A cool way of seeing this is with a chained `or` expression. `or` expressions will evaluate to the *first* truthy value they encounter. So:

```python
False or None or 6
# => 6
```

The first two values are ignored, but the `int` 6 is truthy, and therefore the result of the `or` expression.

Put simply, `None` will evaluate like `False` in comparisons.
