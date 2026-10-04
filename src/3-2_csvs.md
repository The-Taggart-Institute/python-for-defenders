# 3-2: CSVs

Comma Separated Value files are probably the single most common file format you'll work with when parsing data. You'll also encounter a lot of PDFs, but PDFs are not a file format; they are torment engines meant to visit suffering upon the human race. So for now, we'll stick with CSVs.

Are CSVs that complex? Not really. They're lines of text with fields separated by commas. We could make do with the tools we've already learned, but we don't have to. Turns out that Python has a fantastic `csv` module that makes working with this file type incredibly simple.

For this exercise, I've provided a CSV of ransomware IOCs, sourced directly from [US-CERT #StopRansomware alerts](https://www.cisa.gov/uscert/ncas/alerts).

Let's take a quick look with the shell command `head`.


```python
!head ransomware_iocs.csv
```


So we have a header row showing us 3 columns: `Indicator`, `Type`, and `Ransomware Family`. 

You might be thinking we could use our `Indicator` class from Part 1 to give these some structure when we import them. And you're not wrong! But let's focus on the CSV itself for now.

To work with these files in Python, we'll begin by importing the `csv` module. Then we'll use the `dir()` function to see what's inside.


```python
# Import the csv module
import csv

# Let's inspect it
dir(csv)
```

## Reading

There's a lot going on, but of particular interest* to us are the following classes and functions:

* `reader()`: Produces a generic CSV reader from a file object
* `writer()`: Produces a generic CSV writer from a file object
* `DictReader()`: Produces a reader that uses dictionaries to maintain headers
* `DictWriter()`: Produces a writer that writes using dictionaries for headers

Readers are iterators over the rows.

As always, this will make more sense in context. We use the readers and writers in the `with` block.


> [!NOTE]
> Yes I see the `excel` options. I don't care because working with Excel files is awful. Plain text 4 Lyfe.


```python
# Get data with a basic reader()

with open("ransomware_iocs.csv") as f:
  iocs = [row for row in csv.reader(f)]

# Check out the first 10
iocs[0:10]
```

So what did we get? We got ourselves a list of lists. So the `csv.reader` broke down the file and split each row into a list of values. 

> [!NOTE]
> The header is included as the first row, so if you're expect just the data, you'll want to slice off the first element, like `iocs[1:]`.

Now let's see how `DictReader` works.


```python
# Get data with a DictReader()
with open("ransomware_iocs.csv") as f:
  iocs = [row for row in csv.DictReader(f)]

# Check out the first 10
iocs[0:10]
```

Whoah! So instead of a header row in our list, `DictReader` detected the header and used it as keys to create a list of `dict`s! 

This is almost always how I import CSVs. The `dict` provides just enough structure to be useful without needing the whole overhead of a class.

Also, as we'll see in a later section, lists of keyed-alike `dict`s play very well with our data analysis library of choice.

## Writing

Writing is a very similar process. `writer()` expects a list of lists. You can either loop through the outer list and call `writer.writerow()`, or you can do them all at once with `writer.writerows()`. It depends on if you need to do any modification to the list before you write it.

And `DictWriter?` Same deal, but it expects a list of keyed-alike `dict`s.

Let's create some test data in both shapes to play with.


```python
# Create sandbox data

ship_list: [list] = [
  ["Name", "Registry", "Class"],
  ["Enterprise", "NCC-1701", "Constitution"],
  ["Reliant", "NCC-1864", "Miranda"],
  ["Voyager", "NCC-74656", "Intrepid"],
  ["Discovery", "NCC-1034", "Crossfield"] 
]

# If you think I'm writing that out twice you're crazy
ship_dict: [dict] = [ {"Name": s[0], "Registry": s[1], "Class": s[2] } for s in ship_list[1:] ]
```

Finally, a dictionary comprehension in action! That's the kind of Python dorkery I love to do.

Okay, let's write these out.


```python
# First, with the writer()

with open("ships.csv", "w") as f:
  writer = csv.writer(f)
  writer.writerows(ship_list)
    
# And check the results
! cat ships.csv
```

Now `DictWriter` has a bit of a gotcha. It requires a `fieldnames` named argument. We can extract the fieldnames from any one of our `dicts` with the `.keys()` method.

Additionally, if you want the header present, you need to separately call `.writeheader()` before `.writerows()`.


```python
# Now with DictWriter()

with open("ships.csv", "w") as f:
  # Get fieldnames from the first element
  fieldnames = ship_dict[0].keys()
  # Notice the named arg
  writer = csv.DictWriter(f, fieldnames=fieldnames)
  # Write the header, then the wrows
  writer.writeheader()
  writer.writerows(ship_dict)
    
# And check the results
! cat ships.csv
```


```python
# Cleanup the folder
! rm ships.csv
```

No dedicated check for understanding for this section, as we have more file formats to cover! But feel free to play a bit more with CSVs in another Notebook!
