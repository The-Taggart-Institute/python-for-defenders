# 3-3: JSON

**J**ava**S**cript **O**bject **N**otation is a common format for transmitting data over web APIs. Much like `dict`s, they are key-value pairs. In fact, Python's `json` modules takes advantage of this symmetry to easily read/write JSON data!

Now, instead of recreating a new sample file, why not use the one we already had from the last section? Let's reuse the `csv` module to import the IOCs as `dict`s.


```python
# Produce a handy sample data set with the file from the last lesson
import csv

# Grab the file from the previous section. It's my course; I'll do what I want
with open("../3-2_csvs/ransomware_iocs.csv") as f:
    reader = csv.DictReader(f)
    iocs: [dict] = [i for i in reader]

# Show a sample
iocs[0]
```

With the IoCs imported as `dict`s, we can easily make JSON out of them. We'll start by using `json`'s `dumps` function, which produces a string representation of a JSON-able object. Our `iocs` list absolutely qualifies.


```python
# Use json to JSONify our IoC list
import json

# Here comes a wall of text
json.dumps(iocs)
```

That's a lot of text!

What matters here is we now have a well-formatted JSON string. We can write this to a file (but there's actually an easier way), but we can also send this over network connections—say, to an API endpoint.

## Writing Files

The `json` module makes it even simpler than `csv` to write files. The `dump()` method takes a file object and writes the entire JSON-able object to the file.


```python
# Write our IoCs to a file

with open("ransomware_iocs.json", "w") as f:
    json.dump(iocs, f)
```

Now we have a new `.json` file in this folder! It's that simple.

I will also call out that `json.dump()` has an `indent` argument that will make the resulting file formatted with indendation and line breaks for human readability. Open this next file up in a text editor to see.


```python
with open("ransomware_iocs_pretty.json", "w") as f:
    json.dump(iocs, f, indent=4)
```

Quite the difference, right?

## Importing JSON

The `json` module has equivalent reading functions to its writing functions. `load()` loads JSON data directly from file pointers into Python objects, and `loads()` will do the same with strings.


```python
# Quick demo of loads
# Note that JSON requires double quotes, so we enclose the str in single quotes
json.loads('[{"foo":"bar"}]')
```


```python
# Now, let's reload the ransomware IoCs directly from the file

# We start by deleting the iocs variable to remove all doubt
del iocs

with open("ransomware_iocs.json") as f:
    iocs: [dict] = json.load(f)
```

If it seems like working with JSON is a lot easier than working with CSVs...you might not be wrong. But not all data types can be stored as JSON! Anything not [supported by JSON](https://www.w3schools.com/js/js_json_datatypes.asp) has to be stringified one way or another to be saved as JSON.

Again, no need for a check for understanding yet—we're saving that all for the final lab for this section 😉

Up next, we take a brief detour into regular expressions!


```python
# Cleanup the files

! rm ransomware*.json
```
