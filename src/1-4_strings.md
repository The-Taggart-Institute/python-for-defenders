# 1-4: Strings

<iframe style="width: 800px;height: 500px" src="https://www.youtube.com/embed/iqRQokcGEe4?si=ATkScm2lsTLZYm5x" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

We've technically already seen this data type, since we wrote `"Hello, World!"`. Strings (`str`) are Python's primary representation of text.

```python
type("Python")
# => str
```

Strings can be in single quotes or double quotes, but for this course, we'll standardize on double quotes.

## Sequences

Strings are a type of data known as **sequences** in Python. We'll see others shortly. Broadly, sequences are values made of smaller individual elements. In the case of strings, the elements are characters. Sequences are **indexed**, meaning the individual components can be accessed.

### Indices

Sequences are indexed, like addresses on a street. The addresses begin at `0`. So for the string `Python`, the indices go:

```
P Y T H O N
0 1 2 3 4 5
```

To access a specific index, you can use the square bracket notation.

```python
msg: str = "Python"
msg[0]

# => 'P'
```

Indices can also go backward, which is the Pythonic way of accessing the last element of a sequence.

```python
msg[-1]

# => 'n'
```

### "Slicing" Strings

The square bracket notation actually has three potential parameters, separated by colons. The full syntax is:

```
seq[start:end:step]
```

Where `seq` is the sequence being indexed, `start` is the starting index, `end` is the ending index (non-inclusive), and `step` is the interval. We can use this syntax to "slice" the sequence. That's a bit confusing until we put it all into practice. Let's try an example with all three parameters used.

```python
"0123456789"[1:8:2]

# => '1357'
```

We begin at index 1, the second character in the string. We continue up to index 8, but we move by steps of size 2, meaning we take every other character. The result is `1357`. When the `end` parameter is omitted, it is assumed to be the end of the sequence. When `step` is omitted, it is assumed to be `1`. You can also omit `start` and assume it to be `0`. 

`step` can also be negative.

```python
"0123456789"[::-1]
```

That's a common way to reverse sequences.


## Concatenating Strings

**Concatenation** is the connecting or joining of items in a chain—or a string. We commonly want to build new strings out of pre-existing ones. Let's say we have a variable `name`, and we want to create a greeting message. We can concatenate the `name` with a `greeting` to produce a final message. In Python, `+` is the string concatenation operator.

```python
name: str = "Asmodeus"
greeting: str = "Welcome, "
message: str = greeting + name + "!"
print(message)

# => Welcome, Asmodeus!
```

So `message` is a string resulting from the concatenation of `greeting`, `name`, and an exclamation point.

## Format Strings

Concatenation isn't the only game in town for making new strings out of old strings. **Format strings** allow us to place variables directly inside of a "template string."

We prepend the quotes of a format string with `f` to indicate it's a format string.

Let's revisit the greeting example with a format string.

```python
name: str = "Asmodeus"
message: str = f"Welcome, {name}!"
print(message)

# => Welcome, Asmodeus!
```

Little cleaner, right? Fewer variables to keep track of. Whenever possible, I would use format strings when creating combination strings. They tend to be easier to maintain in the long run.

Oh, one more cool thing: the values inside of a format strong don't have to be strings. They can even be expressions!

```python
x: int = 5
y: float = 3.0
message: str = f"The sum of {x} and {y} is {x + y}"
print(message)

# => The sum of 5 and 3.0 is 8.0
```
