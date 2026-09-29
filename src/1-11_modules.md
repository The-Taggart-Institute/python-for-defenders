# 1-11: Modules

So far, we have stuck to Python code that we've written ourselves inside these Notebooks—or whatever's built into Python. But there's a wide universe of Python code out there to explore and take advantage of. We may even want to package some of our code the same way. That's why we need to understand Python **modules**.

Simply put, modules are packages of Python code that we can **import** into our project or notebook.

We'll begin with an out-of-the-box Python module, like `random`.

## Syntax

Python has plenty of additional modules, which you can review in the [Library Reference](https://docs.python.org/3/library/index.html). We'll play with `random` for the moment.

To import an entire module, we can simply `import` the module name.

```python
import random
random?
```

The `random` module is useful for, y'know, random stuff. Like random integers/floats, or even a random choice from a sequence.

When the entire module is imported, its constants and functions reside under the `random` **namespace**. That means to access the `choice()` function, we would refer to `random.choice()`.

> [!NOTE]
> Even though this uses dot notation like classes, `random` is *not* a class. It's just that Python uses the same syntax to access the namespace of modules and classes.

```python
# A random, namespaced choice
random.choice(["Klingons", "Romulans", "Borg", "Oh my!"])

# => ???
```

But importing `random` brings the whole module along. We may want to be more specific with our imports. To do that, we can use the `from...import` syntax. Instead of importing everything, we just import what we want. When constants and functions are imported this way, they are not namespaced—instead, they are directly available.

```python
# Instead of importing everything, just get what we need.
from random import choice

# Look Ma! No namespace!
choice(["Klingons", "Romulans", "Borg", "Oh my!"])
```

## Installing Modules

As rad as Python is out of the box, you'll likely want to install somebody else's code eventually. It's not hard! In fact, you can even do it from directly within a Notebook if you want.

This is kind of an aside, but a cool trick that Jupyter can do is executing shell commands from within a notebook. All it takes is prepending the command with a `!` (bang). Watch:


```python
# List the contents of our repo
! ls ../
```

We can even save the result to a variable!

```python
stuff: list = ! ls ../
stuff
```

Amazing, right? More on that later. But for our purposes, that means we can install packages directly from notebooks. If you're not in a virtual environment, you might just use the `pip3` package manager directly. But we *are* in a virtual environment. What's more, we're using `uv`. We can either run `uv add` or `uv pip install` to add the package to our venv.

```python
! uv add requests
```

In our case it was already there, but the principle is sound. Once the package is installed, we can import it.

```python
# A very naive web request
import requests

r = requests.get("https://taggart-tech.com")
r.text

# => A lot of HTML
```

## Creating Modules

Not all our Python code has to live in the Notebook. In fact, it's probably a good idea that most utility functions, classes, etc. live elsewhere. A good rule of thumb is: if the code should be modified by users on each run of the notebook, leave it in. If it's small and helps the reader/runner understand the Notebook, also leave it in. If the code never changes and just needs to exist for the Notebook to work properly, get it out.

Luckily, basic module creation is as simple as making a new `.py` file and chucking your code in there. You can them import with `import filename` without the extension. Just try not to use the same filename as a real module you'll also want to import, or a function you're already using. For example, do not under any circumstances make a `print.py` file. 

```python
import print

# Sure you have a stuff function in there, but AT WHAT COST?!
print.stuff()

print("This won't work now")
```

You'll have a bad time.

### `__init__.py`

Hey look! Dunders again! 

If you want to make a folder full of Python files but only import with a single statement, it can be helpful to use the [Package structure](https://docs.python.org/3/tutorial/modules.html#packages). There's a lot to this, but broadly, `__init__.py` inside a folder makes Python treat the folder as a module. Any `.py` files inside that folder can be imported via dot notation.

Imagine I have a folder call `mymod` and a file inside called `foo.py`. And inside that file is a function called `bar()`. If the folder had a blank `__init__.py`, I could import that function with:

```python
import mymod.foo

mymod.foo.bar()
```

But what if I wanted to make it easier to access my submodules?

Alternatively, I could bring the submodules into the top namespace with `from...import`:

```python
from mymod import foo

foo.bar()
```

Lastly, if wanted to defined what importing *everything* from my module really meant, I would add a definition of the magic `__all__` list to my `__init__.py`.

```python
__all__ = ["foo"]
```

This allows me to import everything defined in that list with `*`.

```python
from mymod import *

foo.bar()
```
