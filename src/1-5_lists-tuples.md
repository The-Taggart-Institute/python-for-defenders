# 1-5: Lists and Tuples

<iframe style="width: 800px;height: 500px" src="https://www.youtube.com/embed/NtkNuL1gqgY?si=FMz3DV8b-fQ8SGk-" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

More sequences! As we mentioned before, strings are one example of a larger class of data types in Python called sequences. We'll have to revisit one of the core characteristics of sequences in a later chapter, but we can introduce two more sequence types.

## Lists

Lists are exactly what they sound like: a list of things. Just as strings are made of characters, lists are made of **elements**. Lists can contain any data type, and a mix of them.

Lists are surrounded by square brackets and each item in a list is separated by a comma.

```python
stuff: list = [1, "two", 3.0, False, ["a", "nested", "list"]]
```

Yes, even other lists. Accessing items is identical to accessing characters in strings.

```python
stuff[2]

# => 3.0
```

The same slicing syntax we saw for extracting parts of a sequence, or even reversing it, also works with lists.

So what's new with lists? Other than containing more than just text, lists also possess special **methods**—built-in functions that allow us to interact with them.

## Length

The built-in `len()` function measures the length of any sequence, including strings and lists.

```python
len([1,2,3])
# => 3
```

### Adding Stuff

The most common way to add to a list is with the `.append()` method. That adds an element to the end of a list.

```python
# Did you think they would all be Trek?
x_men: list = ["Cyclops", "Jean Grey", "Professor X", "Wolverine", "Beast"]
x_men.append("Rogue")
x_men

# => ['Cyclops', 'Jean Grey', 'Professor X', 'Wolverine', 'Beast', 'Rogue'
```

There's also `.insert()`, which will insert the value at a given index.

```python
x_men.insert(3, "Gambit")
x_men
# => ['Cyclops', 'Jean Grey', 'Professor X', 'Gambit', 'Wolverine', 'Beast', 'Rogue'
```

## Checking Membership

We commonly want to know whether a certain value is in a list. Python has the `in` operator for just such an occasion. We build `in` expressions like using other comparisons, with the element we're checking on the left and the list on the right.

```python
"Cyclops" in x_men
# => True
```

> [!NOTE]
> The `in` operator works with all sequences—including strings!

### Removing Stuff

The `.pop()` method removes the last item from a list and returns it. The return means the value is made available for assigning to a variable.

```python
# Oh no! The Sentinels got the last X-Man!
captured: str = x_men.pop()
print(captured)
print(x_men)
# => 'Rogue'
# => ['Cyclops', 'Jean Grey', 'Professor X', 'Gambit', 'Wolverine', 'Beast']
```

`.pop()` can also be given a specific index to pop instead of the default last position.

```python
wolverine = x_men.pop(4)
print(wolverine)
print(x_men)
# => 'Wolverine'
# => ['Cyclops', 'Jean Grey', 'Professor X', 'Gambit', 'Beast']
```

There's also `.remove()`, which removes the first item (left to right) from the list that matches the provided value. That can get tricky when there are duplicate values. And remember, unlike `.pop()`, `.remove()` **does not return the removed element**.

```python
x_men.remove("Cyclops")
x_men
# => ['Jean Grey', 'Professor X', 'Gambit', 'Beast']
```

## Tuples

Another type of sequence closely related to lists is **tuples**. Instead of square brackets, tuples are surrounded by parentheses.

Tuples are **immutable**. Once you make them, that's it. No `.append()`, no `.pop()`, no `.insert()`, no `.remove()`. They exist as created. Sometimes that's exactly what you want though! And technically, tuples are less memory-intensive, since they don't come with all that baggage. Here's a simple tuple:

```python
coordinates: tuple = (44.5898641,-104.7157436)
# Wonder where that is?
```

Tuples are still indexable, just not changeable.

You'll frequently see tuples in the middle of workflows. Two built-in Python functions produce tuples: `enumerate()` and `zip()`. `enumerate()` takes a list and produces, well an `enumerate` object. That's not super helpful yet, but we can make it a list for us to review.

```python
list(enumerate(x_men))
# [(0, 'Jean Grey'), (1, 'Professor X'), (2, 'Gambit'), (3, 'Beast')]
```

Lots going on here. First, we see our first **type conversion**. You can use the name of a data type as a function to try to convert one data type to another. You'll commonly see this with converting `str` to `int` or vice-versa. Here, we convert the `enumerate` object into a `list` so we can see what we made. The resulting list has the same number of elements as before, but each element is a tuple. Each tuple is a pair of the former list's index and value.

`zip()` works similarly, but it takes two sequences and joins them together as tuples.

```python
powers = ["telekinesis", "telepathy", "exploding cards", "is blue and furry"]
list(zip(x_men, powers))
# => [('Jean Grey', 'telekinesis'), ('Professor X', 'telepathy'), ('Gambit', 'exploding cards'), ('Beast', 'is blue and furry')]
```

A quirk of `zip()` is that the sequences don't have to be the same size. `zip()` will stop producing items after the shorter sequence is exhausted.

```python
list(zip(x_men, "abc"))
# => [('Jean Grey', 'a'), ('Professor X', 'b'), ('Gambit', 'c')]
```
