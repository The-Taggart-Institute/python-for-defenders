# 2-4: LAB | File Hash Generator

Now that we have some of these widgets in our toolbelt, we're ready to make our first real tool: a file hash generator! Is it a little contrived: maybe, but we can build this in such a way that it'll be pretty useful. 

## Features

Our generator will be able to:

* Accept multiple files
* Show MD5, SHA1, SHA256, and SHA512 hashes all at once
* Display results in a clean manner

Not so bad, really. Even though there are command line tools that do this, a little user interface ergonomics goes a long way.


> [!NOTE]
> This is the first Lab of Part 2. The BEST WAY to use this Notebook is to recreate the tool in your own Notebook. Use this as a guide, but produce the working tool for yourself!

## File Hashes in Python

If you're in this course, there's a reasonable expectation that you're familiar with the general concept of file hashes. If you need a refresher, check out [this article from SentinelOne](https://www.sentinelone.com/cybersecurity-101/hashing/).

To make hashes in Python, we have to use the `hashlib` module. Let's import it and start playing with it.


```python
import hashlib
```

`hashlib` is a very powerful module, but let's dig down into the `sha256` function first.


```python
hashlib.sha256?
```

Okay, so it returns a "hash object," whatever that is. And we can give it a string (actually a bytestring) to kick it off. We'll use the string `Python Rocks!` for our test.

Before we do the Python version of this, let's use Jupyter's shell superpowers to get the Linux command line version for reference:


```python
# Use Jupyter's ability to run shell commands to get the sha256 hash of our test string
! echo -n "Python Rocks!" | sha256sum
```

Cool. Now let's try the same thing with Python. Don't forget, we need to use a `bytes` object, so watch for that `b""` syntax.


```python
# Hashing, Python style
test_hash = hashlib.sha256(b"Python Rocks!")
test_hash
```

Uh, what.

Okay so we got back the `HASH object`, but that doesn't actually tell us anything useful. Let's inspect the object a bit more.


```python
test_hash?
```

The two methods that look promising for our purposes are `digest()` and `hexdigest()`. If you look closely at the result of the Linux `sha256sum` command, the characters are all hexademical digits. That should be a hint as to which one we want here.


```python
# Get the proper value from our hash object
test_hash.hexdigest()
```

Look at that! Our `hexdigest()` matches! Now that we know how to generate hashes, the next step is to upload some files. I've provided 2 sample files here for you to play with.

## Upload Files

To make the file uploading easy, let's provide an upload widget. And of course, import the required modules.

We're also going to use a nice HBox widget for clean layout of the upload and the label.


```python
# It's importin' time
from IPython.display import display
import ipywidgets as widgets
```


```python
upload = widgets.FileUpload(multiple=True)
label = widgets.Label(value="Upload sample files here 👉")
hbox = widgets.HBox([label, upload])
display(hbox)
```

## Generate Hashes

With the files uploaded, we can generate hashes for each. There are lot of ways to write this code. Given that we'll need the same data—md5, sha1, sha256, and sha512 hashes—for each file, my move would be to write a `generate_hashes()` function. The function will return a `dict` with hash types as keys, to make our results easy to work with.

I'm going to write this function in a very me style, meaning the code will balance succinctness with readability, but try to minimize intermediate variables. You do not have to write this way.


```python
# Define the `generate_hashes()` function

def generate_hashes(sample: bytes) -> dict:
  """
  Generates a dict of hashes for a given bytes sample
  """
  return {
    "md5": hashlib.md5(sample).hexdigest(),
    "sha1": hashlib.sha1(sample).hexdigest(),
    "sha256": hashlib.sha256(sample).hexdigest(),
    "sha512": hashlib.sha512(sample).hexdigest()
  }
```

With the function defined and our files uploaded, all we need is some code to grab the hashes. We'll once more take advantage of nested dictionaries.

Now, we can do this with a `for` loop, but we can actually expand on a trick we already know. We've seen that list comprehensions are a fast way to make a new list from an existing list. Well, turns out there is also a **dictionary comprehension** that allows us to create new dictionaries from existing ones! Since we have a dictionary from the Upload widget, we can take advantage of this trick to quickly generate a new `dict` with filenames as top-level keys, and the result of `generate_hashes()` as the values for each.

To get the right data shape for this, we use the `dict`'s `items()` method, which provides a sequence of tuples of shape (`key`, `value`) for each item in the `dict`. We can then use those values in our comprehension.


```python
# Quickly make our file_hashes with a dict comprehension
file_hashes: dict = { key: generate_hashes(value["content"]) for (key,value) in upload.value.items() }
file_hashes
```

Rad, so we have our hashes! Now, how to display them? Ideally I'd want a nice clean table. Luckily, there is an HTML widget that will allow us to create just such a thing.

As a refresher, HTML tables are structured like so:

```html
<table>
  <tr>
    <th>Column Header 1</th>
    <th>Column Header 2</th>
  </tr>
  <tr>
    <td>Table cell</td>
    <td>Table cell</td>
  </tr>
</table>
```

We can build up our table with the power of string concatenation. We'll loop over the keys in `file_hashes` to get our data.


```python
# Build our HTML table

table = "<table>"
table += "<tr><th>File Name</th><th>MD5</th><th>SHA1</th><th>SHA256</th><th>SHA512</th>"

# Use a loop over file_hashes to access what we need and add to the table
for f in file_hashes:
  table += f"<tr><td>{f}</td>"
  # Use another loop for the hashes
  # Note we access the dict with the key `f`
  for h in file_hashes[f]:
    hash = file_hashes[f][h]
    table += f"<td>{hash}</td>"
  table += "</tr>"
table += "</table>"
```

Widget time! Let's display our hard work with an HTML widget:


```python
html = widgets.HTML(value=table)
display(html)
```

And that's it! You can of course add some `<style>` in there to change up the appearance. But you now have a file hash generator that will create multiple hash types for as many files at once as you like!
