# 3-1: Opening Files

It might seem a little silly to cover opening files _after_ going through all that work with widgets. But there are going to be plenty of times when we want to open files without a widget. Widgetlessly. That's an adverb now.

## Plaintext vs. Binary

Most of the files we'll deal with are **plaintext** files. Put another way, files we can read with `cat` or a simple text editor. That's the kind of file we'll be focusing on in this lesson. There are plenty of modules that allow us to manipulate more complex filetypes like PDFs or images, but we'll get to those later.

## `open()` and `close()`

Python has a built-in function called `open()` that will access the data at a given path on the filesystem. Open has a few optional arguments, but to simply read a plaintext file, we can simply use `open(<path>)`. You might think this would automatically give us `str` or `bytes` data, but nope! This creates a `TextIOWrapper` object which has additional methods to access its contents. `read()`, for example, will read in the content as a `str`.

Once we've finished doing whatever we want with the file, we would call the `close()` method on the IOWrapper to clean up. Check it out.


```python
# Opening and reading files the long way with open() and close()
f = open("indicators.txt")
data:str = f.read()
f.close()
data
```

## The Shortcuts: `with` and `readlines()`

If this seems like it's setting us up for a bunch of extra work...it kinda is. Luckily, Python has a few more tricks to make working with files a bit easier.

The `with` syntax allows us to open the file and have it automatically closed after we've finished with whatever we want in the `with` block. This structure is for designating temporary resources for a block of code. However, any variables we make inside this block are _not_ temporary.

Another handy method I use is `readlines()`. Where `read()` will produce a single string of data from a file, `readlines()` will produce a list of strings representing the lines of a plaintext file.


```python
# Getting lines the quick way
# Note the with...as syntax
with open("indicators.txt") as f:
  data: [str] = f.readlines()

# And outside of the with block, we still have data
data
```

You may have noticed that our list items came with the `\n` attached. That is going to be annoying later on, so my normal process of importing text data adds uses a list comprehension and the `strip()` method with `readlines()` to remove those trailing linebreaks.


```python
# Same process, but with a list comprehension and .strip()
with open("indicators.txt") as f:
  data: [str] = [l.strip() for l in f.readlines()]
data
```

Burn this pattern into your brain. You'll use it constantly.

## Writing Files

We can use the same pattern to write files, but we need to give `open()` an additional argument: the open mode. By default, this is `"r"`, for read. However, we can also open in `"w"` for write, or `"a"` for write-append. What's the difference? Write will overwrite the contents of a file with new data, while write-append will add on to existing data. You can check out all the open modes in the [Python Docs](https://docs.python.org/3/library/functions.html#open).

Either way, we can use the `.write()` method of the file object to send string data to the file.

Let's try it out.


```python
# Write a file, then show the result
msg_1: str = "I'm written first"
msg_2: str = "I'm written second"

with open("example.txt", "w") as f:
  f.write(msg_1)
    
!cat example.txt
```


```python
# Now let's overwrite it
with open("example.txt", "w") as f:
  f.write(msg_2)
    
!cat example.txt
```


```python
# Append to a file
with open("example.txt", "a") as f:
  f.write(msg_1)
    
!cat example.txt
```

Notice that `write()` did not automatically add a new line on that append. `write()` is fairly primitive, so if we want our lines to be, y'know, lines, we can either loop through, concatenating our string with `"\n"`, or we can use the `.join()` trick to join a list of strings. Watch this:


```python
# Join a list of strings with a newline as the separator
"\n".join([msg_1, msg_2])
```


```python
# Use that .join() trick to write the file
# Append to a file
with open("example.txt", "w") as f:
  f.write("\n".join([msg_1, msg_2]))
    
!cat example.txt
```


```python
# Cleanup the example file
! rm example.txt
```
