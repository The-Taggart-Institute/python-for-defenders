# 3-4: Regular Expressions

I want to be very clear: this is not an introduction to regular expressions in general. If you need to review the basic concepts, I recommend going through our [free regex course](https://learn.taggart-tech.com/p/intro-to-regular-expressions) first. For a quicker review on syntax, check the [Python docs](https://docs.python.org/3/library/re.html).

Instead, we'll review how to use regular expressions in Python, and how they become useful in common defensive tasks.

It all begins with the `re` module, so let's get that imported.


```python
# Import the re module
import re
```

## Defining Regexes

The first method to learn in the `re` module is `re.compile()`, which will take a string and turn it into a Regular Expression object to be used for pattern matching.

This isn't _technically_ necessary, as we'll see, but it's a good practice because it makes the matching process more efficient when reusing the pattern.

We'll start simple with a pattern for email addresses. What will we need?

An email can be any alpahnumeric, dots, and dashes, and underscores (yes, really, even though GMail prohibits them). The name will be followed by an `@` symbol, then a valid domain.

Now since we're dealing with dots, and dots have a meaning in regexes (any character), we'll need to escape them with a backslash. But! Backslashes have meanings in strings for escaping characters already! 

To avoid this weird gotcha, we can use Python's **raw string** syntax to define regexes without any escaping at all. Raw strings are prepending with `r`. Observe:


```python
# Print backslashes with raw strings
print(r"You'd think this would break a line: \n. And yet, it doesn't in raw mode.")
```

So we can use raw strings with `re.compile()` to generate a regex for email addresses. Something a little like:


```python
# Generate the email regex. There are others, but this will do fine for now.
email_pattern = re.compile(r"[a-zA-Z0-9_\-\+\.]+\@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]{2,}")
```

## Matching

With our pattern compiled, we can test this against good (and bad) email addresses to confirm whether it works. To do so, `re` has several methods that work in subtly different ways.

* `.match()` looks for a match against a pattern at the _beginning_ of a string. If there's a match later, too bad. 
* `.search()` looks for the first match _anywhere_ in the string. But only the first.
* `.findall()` will return a list of _all_ matches in the string.

Which one you want is a question of your performance needs, whether you need all matches, and the shape of your data. 

For `.match()` and `.search()`, a `match` object is returned if there were matches. Otherwise, `None` is returned. This can be useful for conditionals based on matches, as you'll recall that `None` is falsy.

To see what was matched, call the `.group()` method.

Let's demo the results of both with a sample of multiple good and bad emails.


```python
# Build our sample
sample: str = "test@test.com testattest.com test@test.c test@bad_domain.com tes+t_1@good-domain.com"

# Test with match
match = email_pattern.match(sample)
```


```python
# Review the findings
match.group()
# => 'test@test.com'
```

So obviously we get one match, but more than one of these should work. Let's try with `.findall()`


```python
# Now try with .findall()
all_matches = re.findall(email_pattern, sample)
all_matches
# => ['test@test.com', 'tes+t_1@good-domain.com']
```

There we go!

## Named Groups

One of my favorite tricks with regular expressions is using named groups. With this regex feature, we get match groups that we can reference using 3 methods: `.group()`, `.groups()`, and `.groupdict()`. The `.group()` method allows one-at-a-time access to named groups; the `.groups()` method returns a tuple of all matches; `.groupdict()` returns a `dict` with the named groups as keys. This in particular can make really quick work of parsing files such as logs.

The Notebook folder has an `auth.log` file for us to play with. Let's import it as lines to process further.


```python
# Import auth.log
with open("auth.log") as f:
  auth_logs = [l.strip() for l in f.readlines()]

# Display them
auth_logs

"""
=>
['10 Oct 2022 15:22:31 - User admin logged in',
 '10 Oct 2022 15:25:10 - User bob logged in',
 '10 Oct 2022 16:02:24 - User admin logged out']
"""
```

If we examine the log—simplistic as it is—and consider what we want out of it, 3 items emerge:

* A `timestamp`
* A `user`
* An `action`

Since each line has a predictable pattern, we can write a regex with named groups to capture the data and save the results. Let's build the pattern.

* The `timestamp` is the beginning of the line, followed by a 2-digit number, a space, a three-character capitalized month, a 4 digit year, and then a HH:MM:SS time
* The `user` is after the string `User ` and followed by a space
* The `action` comes after the space following the `user`.

Capture groups in regexes are delimited by parentheses. In Python, we make named groups with the `(?<name>pattern)` syntax.

Putting it all together now…


```python
log_pattern = re.compile(r"^(?P<timestamp>\d{2} [A-Z][a-z]{2} \d{4} \d{2}:\d{2}:\d{2}) - User (?P<user>[a-z]+) (?P<action>.+)$")
```

> [!NOTE]
> It took me _years_ to be this fluent in regular expressions, and I still make mistakes all the time. If the above is difficult to parse, don't sweat it. Try to break it down one section at a time. I've also created a breakdown of this pattern on [regex101](https://regex101.com/r/0zpfZI/1), which will explain each section and show the matches.

Let's see what we get with a match!

```python
# Test match
match = log_pattern.match(auth_logs[0])
match

"""
=>
<re.Match object; span=(0, 43), match='10 Oct 2022 15:22:31 - User admin logged in'>
"""
```

Now let's see what we get across our three group methods.


```python
# Check .group()
match.group("timestamp")
# => '10 Oct 2022 15:22:31'
```


```python
# Check .groups()
match.groups()
# => ('10 Oct 2022 15:22:31', 'admin', 'logged in')
```


```python
# Check .groupdict()
match.groupdict()
# => {'timestamp': '10 Oct 2022 15:22:31', 'user': 'admin', 'action': 'logged in'}
```

Plainly, we have a successful match! Since our pattern works, we can use it in a list comprehension to quickly parse all the logs.


```python
logs_parsed: [dict] = [log_pattern.match(l).groupdict() for l in auth_logs]
logs_parsed
"""
=>
[{'timestamp': '10 Oct 2022 15:22:31', 'user': 'admin', 'action': 'logged in'},
 {'timestamp': '10 Oct 2022 15:25:10', 'user': 'bob', 'action': 'logged in'},
 {'timestamp': '10 Oct 2022 16:02:24',
  'user': 'admin',
  'action': 'logged out'}]
"""
```

Success! We now have a list of parsed logs in `dict`s.

This method of parsing otherwise difficult-to-parse logs has been invaluable in my defensive work. Another example is this [Apache HTTP log parser](https://github.com/mttaggart/blue-jupyter/blob/main/log-analysis/HTTP.ipynb) from a collection of defensive notebooks I've been cobbling together. There's a lot going on in there which we'll cover shortly.

For now, let's put all this together in our closing lab for this unit!
