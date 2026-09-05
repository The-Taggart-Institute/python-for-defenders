# 1-6: Dictionaries

<iframe style="width: 800px;height: 500px" src="https://www.youtube.com/embed/l-hr51FZeW0?si=oUVOPZtpVkzUHJaO" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


Let's get this out of the way now: the Python data type we're discussing is referred to as `dict` in code. But the full term is [officially](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) "dictionary." Besides, "dict" is...not a great out-loud word. So in here, it's a **dictionary**.

And in truth, the data type *is* a dictionary: the point is to look things up by a point of reference. Except instead of alphabetical order, we can cut right to the thing we're looking for. It's like a dictionary with every word easily bookmarked.

Imagine a list that was a million elements long. Now imagine we were searching for a specific element in that list. If the list has no inherent order (like sorted numbers), we have to just start at the beginning and inspect each element until we get lucky. In the worst case, that takes a million separate operations.


When we have data that we'll want to look up specifically, dictionaries make more sense. They are a type of data structure commonly called **key-value pairs**. The "key", is like a named address of the data, instead of a raw numerical index. The "value" is the data we want to access. Put another way, the key is the thing we know; the value is the thing we're looking for.

## Syntax

Dictionaries are surrounded by curly braces (`{}`). Keys and values are separated by colons, and pairs are separated by commas. It's easiest to see in context. User data is a ready example for the value of dicionaries.

```python
users: dict = {
  "admin": "password123",
  "jhackme": "summer2026",
  "apwnerson": "letmein!"
}
```

To access a given value, you reference the key. So to get Joe Hackme's password, we'd put that username in square brackets after the dictionary name. Remember the key is a string, so we'll need quotes.

```python
users["jhackme"]
# => 'summer2026'
```

## Adding/Removing Items

Dictionaries don't really have `.append()` or `.pop()` methods the way lists do. Instead, to add an item, we simply reference a key with an equals sign. If the key already exists, the value will be reassigned.

Let's add a user.

```python
users["jphishman"] = "superman"
users["jphishman"]
# => 'superman'
```

Removing items is a bit trickier. If you want to blank out the key, you can assign it to `None` or and empty string (`""`). But that can get messy, since it introduces error possibilities in working with multiple data types and unexpected missing values. To delete a key-value pair, we have to use Python's built-in `del` operator, which deletes the value.

```python
del users["jphishman"]
users["jphishman"]

# => KeyError: 'jphishman'
```

You can use `del` with variables as well, but it's rare that you'd want to.

## Keys and Values

Sometimes you just want the keys of a dictionary. Or the values! Dictionaries have both `.keys()` and `.values()` methods that return collections of those, respectively

```python
users.keys()
# => dict_keys(['admin', 'jhackme', 'apwnerson'])
```

```python
users.values()
# => dict_values(['password123', 'summer2026', 'letmein!'])
```

In both cases, we don't get back a `list` exactly. They're special types called `dict_keys` and `dict_values`. But they are easily converted to lists with the same type conversion we've seen before.

```python
list(users.keys())
# => ['admin', 'jhackme', 'apwnerson']
```

## Checking Keys

Just like with lists, the `in` operator lets us check if a certain item is in a dictionary. When you use `in` with a dictionary, the check is against its keys, not its values.

```python
"admin" in users
# => True
```

## Nested Data

It's common to see nested dictionaries, in which a dictionary's values are themselves more dictionaries. That data structure mirrors what we often see in JSON (JavaScript Object Notation) data. Imagine a set of users where much more than just a password is keyed by username.

```python
users: dict = {
    "admin": {
        "username": "admin",
        "password": "password123",
        "first_name": "Admin",
        "last_name": "Admin",
        "enabled": True
    },
    "jhackme": {
        "username": "jhackme",
        "password": "Summer2022",
        "first_name": "Joe",
        "last_name": "Hackme",
        "enabled": True
    },
    "jpwnerson": {
        "username": "jpwners",
        "password": "letmein!",
        "first_name": "Jane",
        "last_name": "Pwnerson",
        "enabled": False
    }
}
```

So to get the full record for the `admin` user, I'd use the `"admin"` key.

```python
users["admin"]
# => {'username': 'admin',
# 'password': 'password123',
# 'first_name': 'Admin',
# 'last_name': 'Admin',
# 'enabled': True}
```

If I just wanted the password, I'd double up on the square brackets, accessing the `"password"` key of the dictionary retrieved at the top-level `"admin"` key.

```python
users["admin"]["password"]
# => 'password123'
```


