# 1-8: Loops

<iframe style="width: 800px;height: 500px" src="https://www.youtube.com/embed/ypBQloHtZgs?si=baIIrU1zrkYPBNYQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Loops are yet another control flow structure, and number 3 in the **4 Fundamentals of Programming**. Computers are all about automation, and automation is all about repetitive tasks. Programs can run as many times as we need, but often specific instructions within a program need to run multiple times as well. Enter loops.

In Python, loops come in two flavors. We have `for` loops when we have a pre-existing collection or sequence for which we want to repeat the same instructions. We also have `while` loops which will repeat the same instructions **as long as** a condition is `True`—or **until** a condition is `False`.

## Syntax

We'll start with the `for` loop. As I said, we can loop over collections, so let's start there.

```python
groceries: list[str] = ["milk", "eggs", "apples", "potatoes", "peanut butter"]
for g in groceries:
  print(g)
"""
=>
milk
eggs
apples
potatoes
peanut butter
"""
```

The `for` keyword begins the loop ceremony. We then create an **iterator**—a variable used to keep track of the current item we're addressing in the loop. I like to think of this as counting on our fingers. Whatever element in the collection is next up in the sequence, that will be the value of the iterator. So for `groceries`, the first value will be `milk`. Then `eggs`, etc. After the iterator comes the `in` keyword, which tells Python to expect a collection. Then the collection. A colon and an indented line after, just like conditionals. Whatever is indented after the `for` line will be part of the loop.

A `while` loop works similarly, but does not take a collection. Instead, it takes a condition, and the iterator is tracked manually.

```python
t_minus: int = 10
while t_minus > 0:
  print(t_minus)
  t_minus -= 1
print("Liftoff!")
```

Here, `t_minus` is the iterator. The `while` keyword expects an expression that evaluates to either `True` or `False`. In this case, a comparison of `t_minus` with `0`. As long as `t_minus` is greater than `0`, the loop will continue.

Note that inside the loop (and indented again), we use `-=` to manually decrement the iterator.

> [!WARNING]
> If you don't handle the iterator, the condition will never change and the loop will never stop. This is a common mistake for new programmers.

## `range()`

Sometimes you just need to loop through a series of numbers. In that instance, you use `range()`. This function produces a **generator** (more on those later) that will produce integers based on the arguments you pass to it. When given one argument, `range()` will provide integers from 0 up to that number. If you give it two arguments, it'll be a start and stop. The start is inclusive while the stop is exclusive. Let's demonstrate.

```python
for i in range(10):
  print(i)
"""
=>
0
1
2
3
4
5
6
7
8
9
"""
```

```python
for i in range(10, 20):
  print(i)
"""
=>
10
11
12
13
14
15
16
17
18
19
"""
```

`range()` can even take a third argument, which works like the interval component of slicing.

```python
for i in range(10,100,10):
  print(i)
"""
=>
10
20
30
40
50
60
70
80
90
"""
```

A common pattern for using `range()` is when you need the index of a thing as well as the value. And we can pair this with `len()` to get the proper size for the range.

```python
crew: list[str] = ["Janeway", "Chakotay", "Tuvok", "Paris", "Kim", "Torres", "Doctor"]for i in range(len(crew)):
  crewmember = crew[i]
  print(f"{i}: {crewmember}")
"""
=>
0: Janeway
1: Chakotay
2: Tuvok
3: Paris
4: Kim
5: Torres
6: Doctor
"""
```

You'll see (and probably try to write) this pattern all the time. But remember, we have `enumerate()` to make this a bit easier. And when the elements of a collection are tuples, Python can handle a two-part iterator.

```python
for i, c in enumerate(crew):
  print(f"{i}: {c}")
```

Isn't that easier?

## Building Collections

Frequently you'll have to produce a string or a list based on a repetitive action, whether from another collection or from some iterative operation. These patterns are well-established, but there are more and less elegant ways to do it.

### Iterative Building

In this pattern, we begin with an empty collection and concatenate/append everything we want.

```python
# Squares of numbers
nums: range = range(1,100)
squares = []
for n in nums:
  squares.append(n * n)
```

We start with an originating collection and a new empty one. Then we use a loop to populate the new list with the result of whatever operation we wish to perform on each element of the original. This is a tried-and-true pattern, and it is a perfectly valid way of building collections.

When building lists and dictionaries, Python gives us another pattern known as **comprehensions**.

### List Comprehensions

Let's produce the same list as above with a list comprehension.

```python
squares: list[int] = [n*n for n in range(1,100)]
"""
=>
[1,
 4,
 9,
 16,
 25,
 36,
 49,
 64,
 81,
 100,
 ...
 9801]
"""
```

Same result, more efficient syntax. The comprehension is an expression wrapped in square brackets. Then, we have the operation first—whatever we want to do to each item in the collection. We need an iterator variable for that operation, so we do this a bit backwards. We use the iterator in the operation, then with the `for` keyword, we name the iterator. Then we state what collection we're using with the `in` keyword.

It takes some practice, but once you get the hang of it, it's an efficient to build lists. I use list comprehensions frequently in my code.

### Dictionary Comprehensions

Turns out you can do the same thing with dictionaries, although the syntax can get a little trickier. Suppose we have a simple list of usernames, but we wanted a richer data structure with both usernames and passwords for each user? A dictionary comprehension can easily create a dictionary of keys from a given list.

```python
users: list[str] = ["admin", "bob", "carol"]
users_dict: dict = {u: {"username": u, password: "changeme"} for u in users}
users_dict

"""
=>
{'admin': {'username': 'admin', 'password': 'changeme'},
 'bob': {'username': 'bob', 'password': 'changeme'},
 'carol': {'username': 'carol', 'password': 'changeme'}}
"""
```

This comes in real handy when reshaping data during certain analysis tasks, especially when we start playing with tools like Pandas later. You'll have a chance to practice the specifics, but for now keep in mind that both comprehension methods can quickly made new collections out of existing ones without the need for a full `for` loop structure.
