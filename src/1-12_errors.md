# 1-12: Errors

Before we move on to the meaty stuff, I want to spent a moment on one of the most important skills you'll develop as a programmer: reading and handing errors.

Errors are going to happen in your code; that's normal and expected—even if at the time they'll make you want to pull your hair out, question your intelligence and purpose in life, right up until you find the stupid bug. Programming is a humbling pursuit, because the computer will not do what you *intended*, only what you wrote. We'll leave aside the inference engines that devour meaning for this exercise, choosing instead to focus on the joy of making something ourselves—including mistakes.

Let's make a mistake together.

```python
# An intentional mistake
x: int = "10" #Whoops
x / 2

# => TypeError: unsupported operand type(s) for /: 'str' and 'int'
```

Something went wrong, hooray! Don't panic. The first thing to remember when errors occur is that **you can fix them**. And the error message is your best chance to do so. 

A Python error, also called an **Exception**, can come in many different flavors. Read the docs on [Exceptions](https://docs.python.org/3/builtins/exceptions.html) to see all the different kinds that are built-in. Third-party modules will have their own as well. In this case, we have a `TypeError`, and a message telling us that we used an "unsupported operand" with `/`. Sure enough, you can't divide a string.

You can also see that the traceback points you right to where Python thinks the error is. This isn't always perfect, but it gets you close (sometimes the issue is a missing comma/indentation above or below).


## Handling Errors

It's all well and good to understand error messages, but we don't want to have to debug a crashing program in production. Good programming is **defensive**, meaning it anticipates and handles potential errors or bad input gracefully. Python gives us a valuable structure for doing so: a kind of control flow known as **try/except**:

The `try/except` block attempts an operation, and then provides "escape hatches" in the event of failures. Multiple types of exceptions can be handled in different branches, and we can also provide alternative instructions if none of those match. We can even provide instructions that run regardless of failure state.

Let's build a common error pattern to test this out: accessing an out-of-range index in a collection.

```python
# The empty list
stuff = []
try:
  thing = stuff[1] #That won't work
except:
  print("That index doesn't exist!")
# => That index doesn't exist!
```

Seemingly simple, but what's important here is that the exception was *handled*. The program did not crash. 

Let's get more specific with our exception handling—one for a bad index, another for a bad list name.


```python
stuff = []
try:
  thing = stuff[0] #Change the list name to something else to see the difference
except IndexError:
  print("That index doesn't exist!")
except NameError:
  print("That item doesn't exist")
```

We're making some guesses about errors to expect, but we may not be able to anticipate them all. We can also name the Exception and refer to it in our code.


```python
stuff = []
try:
  thing = stuff.keys() # Accessing a non-existent attribute
except IndexError:
  print("That index doesn't exist!")
except NameError:
  print("That item doesn't exist")
except Exception as e:
  print(e)

# => 'list' object has no attribute 'keys'
```

We hadn't named that `AttributeError`, but we could use it in our catch-all `except`, which triggered because the more specific `except` clauses above did not.

We can also add code that runs if the attempt is successful in an `else` block, which must come after all `except`s. This is a useful pattern that allows us to isolate the error-prone code in the `try`. You don't want too much in the `try`, or you may catch errors from another step that needs separate handling.


```python
stuff = ["vanadium", "iridium"]
try:
  thing = stuff[0] # Accessing a non-existent attribute
except IndexError:
  print("That index doesn't exist!")
except NameError:
  print("That item doesn't exist")
except Exception as e:
  print(e)
else:
  print(f"Picking up some {thing}")


# => Picking up some vanadium
```

Finally, there's a `finally`! The `finally` clause allows us to execute code regardless of exception state. This can be useful for logging and other operations that should occur in all circumstances.

Mess with different parts of the code below to see how the output differs.

```python
stuff = ["vanadium", "iridium"]
try:
  thing = stuff[0]
except IndexError:
  print("That index doesn't exist!")
  status = "index_error"
except NameError:
  print("That item doesn't exist")
  status = "item_error"
except Exception as e:
  print(e)
  status = "error"
else:
  print(f"Picking up some {thing}")
  status = "ok"
finally:
  print(status)
```

There you have it, a quick and dirty introduction to errors in Python. Learn to love `try/except`—it really will save you lots of time and frustration. One area that's particularly true is in long-running procedures in Notebooks that handle big datasets. You do **not** want to be halfway through thousands of items and have something error out, requiring you to start again. Anticipate the errors, handle them in code, and run the process with confidence.


