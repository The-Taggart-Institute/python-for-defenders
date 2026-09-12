# 1-7: Conditionals

<iframe style="width: 800px;height: 500px" src="https://www.youtube.com/embed/OiN0YTp7qRE?si=n3hHFLvPfZBQyO2w" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Python programs are instructions executed in the order written. At least so far, but that doesn't really give us much flexibility. Sometimes we might want the ability to jump around in our program, to repeat instructions, or to only execute certain instructions under specific conditions. These abilities are known as **control flow**.
**Conditionals** allow us to execute instructions only when a given test passes. Conditionals are the second of the **4 Fundamentals of Programming** we've encountered.

## Syntax

They look like this.

```python
name: str = input("What's your name?")
if name == "Bob":
    print("Hey Bob! Good to see ya!")
else:
    print(f"Nice to meet you, {name}!")
```

Those few lines contain several important concepts and syntax patterns. First, we have the `if` keyword that starts the conditional statement. Then we have the condition, the test that evaluates to `True` or `False`, followed by a colon. The next line is indented. This is the code that will execute if the test passes (evaluates to `True`). It can be more than one line. After that comes the `else` block. Not every conditional statement has one of these; you can simply have an `if` that checks for a `True` state. This one has code that runs otherwise. And again, an indented line. 

> [!NOTE]
> Indentation is *very important* in Python. Other languages use curly braces (`{}`) to delimit blocks of code. Python uses indentation, which means it is both easier to write and easier to mess up. 

We can handle more than one binary state. With `elif`, we can test for multiple conditions in order. Think of this as falling down a ladder. The first test to pass will be the code that executes, even if other conditions are also true.

```python
num: int = int(input("What's the number?"))
if num % 15 == 0:
  print("FizzBuzz")
elif num % 5 == 0:
  print("Buzz")
elif num % 3 == 0:
  print("Fizz")
else:
  print(num)
```

Ah, good ol' FizzBuzz. In this code block, providing a number divisible by 3 *and* 5 (also known as divisible by 15) will result in the first test passing. While one of the other conditions would also be true, that code does not execute because the first test captured the control flow.

Not every `if` needs an `else`, but if you use `elif` intermediate conditions, you *must* end with an `else` to catch all other possibilities.
