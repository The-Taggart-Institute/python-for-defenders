# 1-10: Classes

<iframe style="width: 800px;height: 500px" src="https://www.youtube.com/embed/xp55bwUUwpI?si=AMjm18-l_RUX9rTC" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

> [!WARNING]
> This is going to be a long one. Get a drink or a snack before getting started.

We've just explored building functions, and how to put them together. That can be a wonderfully elegant way to build programs, slowly changing information from one shape to another until we arrive at our destination. But that isn't always the easiest way to think about problems. We're humans, not data pipelines. We think about **things**. We can reason that way in Python too.

Python is an object-oriented program. "Object" has a specific meaning in here. It refers to data structures defined by a specification known as a **class**. Think of a class as a blueprint for that contain both **properties** and **methods**. Properties are characteristics, attributes that are common to a certain kind of structure, but whose values may be unique for a specific **instance**. Methods are functions attached to that object that take usually make use of the object's specific property values.

## Syntax

This makes more sense in practice. Let's build a `User` class to contain information about users in a system.

```python
class User:

  def __init__(self, username: str, password: str):
    self.username = username
    self.password = password
```

So much in so few lines. First, we use the `class` keyword to declare a new class, the name it. By convention, class names are capitalized.

Inside the class, we'll see methods defined. Methods are like normal functions, except they take a special first argument, `self`, which refers to the specific object instance the function's getting called on.

But how do you make instances in the first place? It's all well and good to have a blueprint, but building from it is a different story. That's what `__init__()` is all about. This function is known as a **constructor**. The double underscores (known as "dunders") mark it as a **magic method**. These are methods Python will call under the hood in specific circumstances. This one makes object instances, and is invoked when we call the class name like a function.

### The Constructor

The `__init__()` constructor method, like all methods attached to object instances, has a first parameter of `self`, referring to that specific object. Here we can use **dot notation** to set properties on the object. We are defining two properties (for now): `username` and `password`, both strings. We don't need to do anything special with them, so they are passed right from the function to the property assignment. But that doesn't have to be the case! Constructors can perform validation checks, sanitization, or other housekeeping before assigning properties.

Let's make a new `User` instance called `alice`.

```python
alice = User("alice", "password123")
alice
# => <__main__.User at 0x7f23f7eb3d90>
```

Asking for the value of `alice` doesn't tell us much. Luckily, we can access the object's properties.

Both properties and methods use dot notation for access from the object itself. We've already seen this at work with `.append()` on lists, and `.lower()` on strings. Both of those are methods common to all objects of the list and string classes, respectively. Let's access our user's properties.

```python
print(f"{alice.username}: {alice.password}")
# => `alice: password123`
```

## Methods

Wouldn't it be nice if our user objects could _do_ stuff too? Like, what if we wanted a way to easily reset the user's password? If the `User` class had a defined `reset_password()` method, we could do it.

So let's do it. We'll rebuild our `User` class to add our new method, and reinstantiate `alice`.  

```python
class User:

  def __init__(self, username: str, password: str):
    self.username = username
    self.password = password

  def reset_password(self):
    new_pass: str = input("New password:")
    new_pass_confirm: str = input("Confirm new password:")
    if new_pass == new_pass_confirm:
      self.password = new_pass
    else:
      print("Passwords don't match")

# Recreate alice
alice = User("alice", "password123")

#reset password
alice.reset_password()
```

> [!NOTE]
> Yes, I know the function we just wrote doesn't return anything. Sometimes "getters" and "setters" will only make internal changes to the object

This is a fairly contrived example, but now you see how we define and call methods on objects.

### Magic Methods

You know, that format string we used earlier was pretty handy. It'd be nice if that was what we got when we asked Python to `print()` our `User`s. That's doable! We simply need to define (and override) the `__str__()` magic method. That method, which is secretly already attached to our object (we'll understand how shortly), determines what `print()` produces.

Let's go back and once more redefine our `User` class with the following addition:

```python
class User:
  # ...
  def __str__(self):
    return f"{self.username}: {self.password}"
```

Recreate the `alice` object and try to print it out.

```python
print(alice)
# => alice: password123
```

Much nicer.

> [!NOTE]
> Try the `__dict__()` method. What does it do? Is that useful?

## Docstrings

Remember the `help()` methods and the `?` trick in Jupyter? Try that on `alice`.

```python
alice?
"""
=>
Type:        User
String form: alice: password123
Docstring:   <no docstring>
"""
```

Notice the "Docstring" section? Where do those come from?

[Docstrings](https://peps.python.org/pep-0257/) are multiline comments at the very top of modules (files), functions, and classes. By convention, they should either quickly describe what the function does, or do that *and* clearly define parameters.

Let's once more redefine `User`, but with a docstring.

```python
class User:
  """A User with a username and a password."""
  # ...
```

Reinitialize `alice` and use the question mark again:

```python
alice?
"""
=>
Type:        User
String form: alice: password123
Docstring:   A user with username and password
"""
```

You'll want docstrings for most classes, functions, and methods.

## Class Methods and Static Methods

Most of the time, you'll want the functionality related to a class to be object-specific. But *sometimes*, the class itself has some work to do. In that case, we can use **class methods** and **static methods**, alongside **class variables**

### Class Variables (aka Class Attributes)

Let's expand our `User` class to include an `id` property. We want this ID to increment every time we make a new user. That's tricky, because how will the constructor know what the last `id` was? The objects can't communicate that information between each other.

This is exactly what class variables are for. By attaching the information directly to the class itself, rather than a specific instance, the class structure can keep track of the information throughout the run of the program. Let's rebuild the `User` class one more time with a class variable and a new property for the instances.

```python
class User:

  # Our new class variable
  last_id: int = 0

  def __init__(self, username: str, password: str):
    self.username = username
    self.password = password

    # Increment last_id and use it for our id
    User.last_id += 1
    self.id = User.last_id

    # A cleaner output for our users
    def __str__(self):
      return f"""ID: {self.id}
Username: {self.username}
Password: {self.password}""""

    # Rest as before...

```

So we've added `last_id` to the `User` class itself. When `__init__()` runs, it increments that value and uses it for the `id` of the newly-constructed `User` object. The next time the constructor runs, `User.last_id` will have that new value ready and waiting.

While we were making changes, I went ahead and added the `id` value to the string representation of the object. Notice that I used a multiline string, making a nice clean output for out information.

Try it out: make two users and see how they look.

```python
alice = User("alice", "password123")
bob = User("bob", "letmein")

print(alice)
print(bob)
```

Sure enough, the `id`s increment.

### Static Methods and Class Methods

Methods we've seen so far attach directly to the objects we make. But there are situations in which we need helper functions that don't have to exist on *every* object, but still make sense within the class container.

If such a helper function needs access to data stored in the class (aka a class variable), we will create a **class method**. If it's just a utility function that doesn't access class variables, we will make a **static method**. What's the difference?

Two things: a parameter and a **decorator**. Let's make both and you'll see.

First up, a class method to make a blank reference user without updating the `last_id`. Modify `User` by adding the below function, including the `@classmethod` line.

```python
class User:

  #...
  @classmethod
  def reference_user(cls):
    new_user = User("notauser", "Password123")
    # Re-decrement the last_id after the constructor incremented it
    cls.last_id -= 1
    return new_user
  #...
```

New syntax! The `@classmethod` decorator is a sort of macro for the function. It allows us to define a function inside the class that doesn't get interpreted as an instance method, which is what Python expects all functions in a class to be otherwise.

The function itself includes a `cls` parameter, which references the containing class. That's how we can access `cls.last_id`.

> [!NOTE]
> Why not just reference `User.last_id`? In this case you could, but as we'll see when we get to **inheritance**, you might not want to hard-code a class name that way.

Now let's add a simple password validator. We won't make the rules too complicated; the important point here is that we have a utility function that makes sense underneath the `User` namespace, but doesn't actually need access to any instance- or class-level information. It's just…in there. For that we'll use a static method. Add the following to our `User` class.

```python
class User:

  #...
  @staticmethod
  def validate_password(password: str) -> bool:
    """Returns true if password is valid per policy:

    1. >= 10 characters
    2. Contains capitals
    3. No spaces
    """
    return len(password) >= 10 and \
      password.lower() != password.upper() and \
      " " not in password
  #...
```

Now our `User` class has a handy `validate_password()` function we can access at any time.

```python
User.validate_password("password")
# => False
User.validate_password("Password123")
# => True
```

## Inheritance

We sometimes encounter the need to distinguish between different variations on a class. They'll all have some things in common, but details will differ. Users can reflect this variation, since a system may have many kinds of users—they'll share some characteristics, but also differ in ability and sometimes even stored data.

We can represent these different user types with **User** of `User`. In fact, we can build our classes such that `User` mostly functions as a **base class** that can be extended or modified for more specific user types. Let's first amend `User` to include a `role` property, and adjust the `__str__()` method accordingly.


```python
class User:
  # ...
  def __init__(self, username: str, password: str):
    self.username = username
    self.password = password
    self.role = "user"
  # ...
    def __str__(self):
      return f"""ID: {self.id}
Username: {self.username}
Password: {self.password}
Role: {self.role}"""
  # ...    
```

Now we can create an `Administrator` user type that **inherits** from `User`. Inheritance is indicated with parenthesis after the class name in the declaration, and the **parent class** or **super class** within.

```python
class Administrator(User):
  """Administrator User"""

  # Stricter controls for admins
  @staticmethod
  def validate_password(password: str) -> bool:
    """Returns true if password is valid per policy:

    1. >= 20 characters
    2. Contains capitals
    3. Contains special characters
    3. No spaces
    """
    return len(password) >= 20 and \
      password.lower() != password.upper() and \
      any([c in password for c in  ["!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"]]) and \
      " " not in password


  def __init__(self, username, password):
    super().__init__(username, password)
    self.role = "administrator"
```

Two changes here, other than the declaration using the `User` class as a parent in the parentheses. First, we **override** the `validate_password` method for the `Administrator` class, because this class has a stricter password policy. Second, the constructor first calls `super()`, which returns the parent class, and invokes its constructor with the arguments passed to `Administrator.__init__()`. Then we modify the role separately for admins.

This is how we can create variations of complicated objects that share significant amounts of structure.

There's some art to thinking in objects when writing code, and not everyone agrees on the best ways to do it. Some people avoid it altogether and stick to writing lots of composed functions. But when a problem naturally fits into object-shaped patterns, you should have the tools to express those ideas clearly, and to make distinctions between super and sub-classes of objects.

