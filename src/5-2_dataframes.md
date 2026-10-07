# 5-2: DataFrames and Series

Now we're ready for prime time. Working with data in Pandas is some of the most important material in this course. Once you know how to do it, it will transform your analysis capabilities. Do not skip this section; do not skimp on this section. It's far too valuable for anything less than your complete attention.

Now then, let's begin.

You've already seen the creation of `DataFrame`s from `list[dict]`-shaped data. Let's explore some other common uses.

## DataFrames from CSVs

This particular pipeline is probably _the most common_ ingestion method to get data into a `DataFrame`. CSV exports of logs, IoCs, etc. are made extra powerful inside of Pandas. Luckily, Pandas has a built-in method called `.read_csv()` that will take a CSV and create a `DataFrame` using a header row for column names.

The CSV we're going to use is a list of domains associated with the [Blackfile/Helix](https://ifin.network/t/blackfile-related-emerging-domains/826) credential stealer campaign. This forms a solid basis for analysis and enrichment.

Let's load that in now and use `.head()` to check it out.

```python
# Import Pandas
import pandas as pd
```

```python
# Use .read_csv() to create our DataFrame
# This may gnerate a DTypeWarning. Don't sweat it.
df = pd.read_csv("blackfile.csv")
```

```python
# Look at the first 5 rows with .head()
df.head()
```

## What's in a DataFrame?

A `DataFrame` contains multitudes. Understanding how each part functions will make manipulating them to do our bidding much, much easier.

### Indices

If you look closely at the output of `df.head()` above, you'll see that just to the left of the `uuid` column, there appears to be an extra column. What gives?! We didn't define that!

Indeed we did not. Every DataFrame requires an **Index**, which is how the individual rows in the DataFrame are referenced. Any column containing unique values can be an Index, but ideally it's one containing sensible sequential values. We can define and `index` column when we create the DataFrame, but if we don't, Pandas will create one for us. Let's look at `df.index` to see what it is.

```python
df.index
```

Indices are important because they are the _way we access rows_. It's important to not think of indices in DataFrames the same way we think of them in a list. They don't really work the same way. Watch what happens when we try to use the list indexing syntax with a DataFrame:

```python
# Try to get the first row...or will we?
df[0]
```

Yeah, that doesn't work. Pandas DataFrames have their own unique syntax for accessing data in this manner, built on two properties: `.loc` and `.iloc`. They look a little strange in practice.

Let's try `.loc` first.

```python
# Access the first row
df.loc[0]
```

But that's not all `.loc` can do. We can pass column names as well after a comma! Let's say we wanted the `value` column.

```python
df.loc[0, "value"]
```

That's all we get! What if we want more than one col? List 'em.

```python
df.loc[0, ["uuid", "Description"]]
```

Okay, but what if we want multiple rows? We can either list them or use a slice syntax.

```python
# Access the first 10 rows
# We can also use a list of index values
df.loc[0:9, ["value", "comment"]]
```

Notice that we get a much nicer output when we select multiple rows.

`.iloc` works similarly, except that it uses integer values for access rather than names. In the case of our Index, they are one and the same, but watch how we can access columns with `.iloc`.

```python
# Using .iloc to access data
df.iloc[0:10, 0:3]
```

In truth, I rarely access data directly in this way. The whole point is to manipulate the data at scale, so it's uncommon for me to need to access specific rows.

But before we depart Indices, I want to stress the value of using a custom Index rather than the default. Depending on your data shape, this can be incredibly convenient. One common example is if your dataset has (completely) unique timestamps. In that case, you can convert the timestamp to a `DateTimeIndex` and have Pandas automatically sort your data chronologically. This also gives you the power to group data by hour, month, day, etc. 

Our data happens to have unique values in the `value` column. So if we wanted to, we could use that as our index. Let's try it and see the difference.

We can change the index of a `DataFrame` with `.set_index()`. I want you to look at the [docs](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.set_index.html) for this method because it introduces a common pattern in Pandas: normally, when we make a global change to a DataFrame, Pandas will return a new DataFrame instead of mutating the original. This is for data integrity and is a good idea! However, if you know for sure you want to change the original, you can often pass `inplace=True` as an optional argument to the method.

But we won't be doing that right now.

```python
# Create domain-based index
domain_idx_df = df.set_index("value")
domain_idx_df.head()
```

Look ma, no integers! This also means that our use of `.loc` will have to change. Let's try for one of my favorites:

```python
domain_idx_df.loc["enroll-passkey.com"]
```

## Series

Take a DataFrame and smash it apart, what would you get? Series! Each column is a Series, but don't think of them as just glorified lists. Each Series has many of the same capabilities as a DataFrame—they even have their own Index!

We can access Series/columns a bunch of different syntaxes. We can use a `dict`-like square brace syntax...


```python
df["value"]
```

…a list of them will work as well:

```python
df[["value", "comment"]]
```

Or we can use a dot notation, if there are no spaces in the column name:

```python
df.value
```

Note that these are printing with an integer column. That's because Series also have an Index, which you normally don't want to mess with. But it's there!

Just take a look at everything a [Series](https://pandas.pydata.org/docs/reference/series.html) has inside of it to give you an idea of the capabilities here.

## Check For Understanding

These won't be tested, but try these challenges yourself to see if you have grasped DataFrames and the basics of data access.

1. Use `.iloc` on `df` to access the `value` and `comment` columns of rows `30-40`.
2. Access just the `comment` Series using dot notation.
3. Access the `value` and `date` Series using brace notation.

And that'll do it for this intro to Pandas! Up next, filtering and data aggregation!
