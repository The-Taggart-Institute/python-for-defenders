# 1-7: Conditionals

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

## Conditional Lab: Password Policy

If you're here, you're probably invested in defensive cybersecurity. It's in the course title! For better or worse, some part of our lives as defenders concerns, yes, Compliance.

And Compliance loves a password policy, oh yes they do. We all know the words; let's sing them together!

🎵 Your password must be… 🎵

🎵 Longer than eight characters 🎵

🎵 But not just alphabetical 🎵

🎵 Be sure to use a capital 🎵

🎵 And digits would be radical 🎵

🎵 And for that extra dash of strength 🎵

🎵 Use symbols to extend the length 🎵

🎵 If you follow these few simple rules 🎵

🎵 Your password won't be guessed by fools 🎵

🎵 And that's the password song!🎵

And now, let's build a conditional tree that tests it!

```python
# Get the password to test
password: str = input("What's the password?")
```

### Length Check

The first check is for length. Python has a built-in `len()` function that will return the length of sequences, including strings. We can use that in our first test.

```python
# Test for length
min_length = 8
if len(password) < min_length:
  print("[-] Length check failed!")
```

### Mixed-Case

The second check is for mixed case (both upper and lower-case letters). For this, we can use the strings built-in `lower()` and `upper()` methods, which will lower-case or upper-case a given string, respectively. Our check can be whether the lower-cased version of the string matches the original `or` the uppercase version matches. Either way, it's a fail.

```python
# Use or to combine 2 checks
if password.lower() == password or password.upper() == password:
  print("[-] Mixed case check failed")
```

### Digits

We need to check for the presence of digits. Now, while Python strings have `isalpha()` and `isalnum()` methods, we can't just use those on our whole password and call it a day. For one thing, these tests will fail if we have special characters in there like we're supposed to. Rather, we need to check to make sure that _at least one_ character is a digit.

There's an efficient way to do this, but it requires a trick we haven't learned yet, so forgive the brief skip-ahead.

Python has a built-in `any()` function that returns `True` if any element of the sequence you give it evaluates to `True`. Watch:

```python
# Any with booleans
any([False, False, False, True])

# => True

# Any with falsy values
any([0, 0, 0])

# => False

# Any with falsy and truthy values
any([0, 0, 1])

# => True
```

So what we need is a list of `True`/`False` values generated from the `password` string. We haven't yet covered repeated actions, so forgive the brief leap, but we'll use a **list comprehension** to apply `isdecimal()` to each character of `password`, and use `any()` on that list to determine if there are digits present.

Since we're testing for their absence, we'll negate the `any()` with `not`.

```python
if not any([c.isdecimal() for c in password]):
  print("[-] Digit test failed")
```

### Symbols

To seek symbols (naively), there's a much easier method we can use. `isalnum()` returns `True` if every character in the string is alphanumeric. This should fail if symbols are present. It's not perfect, but it'll do for now.

```python
if password.isalnum():
  print("[-] Symbol test failed")
```

## Check for Understanding

### Objectives

You have on objective: Combine these checks into a single conditional! Don't forget we begin with `if`, have 0 or more `elifs`, and end with `else`.
