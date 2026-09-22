# 1-9: Functions

<iframe style="width: 800px;height: 500px" src="https://www.youtube.com/embed/Y64iCkhKLaQ?si=Pas6x1oTJZF8IgXC" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

We've arrived at the last of the **4 Fundamental Structures of Programming**, and probably my favorite. **Functions** can be thought of as mini programs within the larger program that we can execute on demand. Anytime we have a task that must be repeated in a program, there's an opportunity to make a function.

## Basic Syntax

Let's build a simple function to make our original "Hello, World!" code repeatable.

```python
def greet():
  print("Hello, World!")
```

Short and sweet. `def` is the Python keyword that begins *defining* a function. Then comes the function name, followed by parentheses—in this case, empty parentheses, but that won't always be so. Then a colon and an indented next line. Anything indented after the function declaration is part of the function.

If you created and executed the cell above, you received no output. That's because **declaring** a function and **calling** or **invoking** a function are two separate operations, just like writing the program and running the program are separate. Another analogy I used to give my students was that declaring a function was like writing a spell down on a scroll, while calling the function was reading it aloud to cast it.

To call the function, we write the function name, followed by the parens and whatever the parens need to contain (hold onto that idea).

```python
greet()

# => Hello World
```

## Parameters and Arguments

What's up with those parentheses, anyway? Just like how we can pass options to programs when we run them, we can provide information to functions to alter their output. When we define these in the function declaration, they are referred to as **parameters**. Think of them as variables we use inside the function whose value we can set when we call the function. Parameters make functions much more useful.

```python
def greet(name: str):
  print(f"Hello, {name}!")

greet("Bob")

# => Hello, Bob!
```

Now our greeting has a `name` parameter of type `str`.

> [!NOTE]
> As always, the type hints are optional. `def greet(name):` is also syntactically correct, but making parameter data types clear is one of **the most important ways** of documenting our code for other programmers.

We can name multiple parameters in a function. Too many gets cumbersome, but sometimes you want to provide more than one adjustable value.

```python
def greet(name: str, punctuation: str):
  print(f"Hello, {name}{punctuation}")

greet("Alice", "!")
greet("Bob", ".")

"""
=>
Hello, Alice.
Hello, Bob.
"""
```

Now our `greet()` function is a lot more flexible. We can provide different **arguments** (specific values for function parameters) to alter the output.

### Default Values and Named Parameters

In the `greet()` function, we have two parameters which are **positional**. We have to provide `name` first, then `punctuation`. But what if we didn't feel like always providing punctuation, since most of the time it will be a period? We can set **default values** for parameters. This allows us to abbreviate the function call when we want to use the default.

```python
def greet(name: str, punctuation: str = "."):
  print(f"{Hello}, {name}{punctuation}")

greet("Alice")
greet("Bob", punctuation="!!")

"""
=>
Hello, Alice.
Hello, Bob!!
"""
```

Naming parameters has an interesting side-effect. If, after our parameters without defaults, we only have parameters with default values, we get to change their order however we like. Let's add a `friendly` boolean parameter to make the greeting more or less friendly.

```python
def greet(name: str, punctuation: str = ".", friendly: bool = False):
  if friendly:
    print(f"{Hello}, {name}{punctuation} It's nice to see you{punctuation}")
  else:
    print(f"{Hello}, {name}{punctuation}")

greet("Alice")
greet("Bob", friendly=True)

"""
=>
Hello, Alice.
Hello, Bob. It's nice to see you.
"""

```

Notice I didn't have to provide an argument for `punctuation`; I could just skip right over to `friendly`. This only works if we have exclusively parameters with defaults following any positionals.

## Returning Values

Up until now, we've been using functions incorrectly. Our `greet()` function has been calling `print()` to generate output, but this short-circuits the intended usage of a function. Functions have a dedicated keyword: `return`, that sends a value back from the function. `return` ends function execution and sends the program back to the function call location. If we want to assign a value to a variable as a result of a function call, or really do anything else with the result of a function, the function *must* return a value.

Printing or any other operation inside the function that produces a change not represented in the return values is known as a **side effect**. We do not like side effects. Our functions' operations should be clear and predictable based on the function signature (parameters and return type).

Let's rewrite `greet()` to properly return a value.

```python
def greet(name: str, punctuation: str = ".", friendly: bool = False) -> str:
  if friendly:
    return f"{Hello}, {name}{punctuation} It's nice to see you{punctuation}"
  else:
    return f"{Hello}, {name}{punctuation}"

greet("Alice")
# => 'Hello, Alice.'
```

Not much has changed—we've replaced `print()` with `return`. However, notice the subtle difference in the output. The value is now in quotes, because we're returning a `str`. Also, did you notice the new type hint at the end of the function definition? We can use a `-> type` before the colon and after our parentheses to indicate the **return type** of the function. Like all type hints, these are optional, but I strongly encourage using them. Knowing what data types a function expects (parameters) and returns goes a long way to keeping track of your data in a Python program.

In Jupyter, returning values also has a somewhat annoying consequence for displaying values. In a cell, Jupyter will display the value of the last expression. If that's a function call, no worries—you'll get the returned value. But if you have two function calls at the end, you'll only see the last one.


```python
# In Jupyter:

greet("Alice")
greet("Bob")

# => 'Hello, Bob.'
```

To address this, you need to bring your own `print()` statements. 

```python
# In Jupyter:

print(greet("Alice"))
print(greet("Bob"))

"""
# =>
Hello, Alice.
Hello, Bob.
"""
```

Both values display. And notice the quotes are gone, because this is the result of printing output, not the display of the expression's value. A subtle difference, but one that will become important as we handle and display multiple function results.

## Function Composition

Some of you may remember this from Algebra. Since functions return values, a function call can be used *directly* as the argument to another function. This is known as **function composition**, and it's an important design approach in many programs.

Let's imagine a function that converts any string into SpongeBob case (wOrDs lOoK lIkE tHiS). It takes in a string and returns a string, and alters the case for each.


```python
def spongebob(msg: str) -> str:
  result: str = ""
  for i, c in enumerate(msg):
    # lower case evens
    if i % 2 == 0:
      result += c.lower()
    else:
      result += c.upper()
  return result
```

What a fun demo function! We have a `for` loop in there, a conditional, and two string methods. This pattern of building a `result` over a loop and returning is one to get comfortable with. Also note we're taking advantage of `enumerate` to get the index and the value of each character in `msg` at the same time.

If we want to SpongeBobify a greeting, we can wrap the call to `greet()` in a call to `spongebob()`.

```python
spongebob(greet("Alice"))

# => 'hI, aLiCe.'
```
