# 5-3: DataFrame Manipulation

Now that we have the basics of `DataFrame`s sorted, we're ready to use Pandas manipulate our data at scale. This is where we use grouping, aggregation

We'll be using a log of DNS queries from [Zeek](https://zeek.org/), courtesy of the [Security Datasets](https://github.com/OTRF/Security-Datasets) repo.

DNS logs are a great example of when we want to use Pandas to analyze aggregated data. These logs will almost always be far too large to review manually.

Our `dns.log` is in fact a JSON file. You might think that means we need to import the `json` module.

But naaaaah, Pandas has a `.read_json()` method. Let's load this `DataFrame` up.

```python
# Import as always
import pandas as pd

# Create our DataFrame
df = pd.read_json("dns.log")
```

## Exploratory Data Analysis

[**EDA**](https://towardsdatascience.com/exploratory-data-analysis-8fc1cb20fd15) is always our first step with a proper dataset. This process gives us a general sense for the size and scope of the dataset, as well as some basic statistical information.

To start, I like to use the `.shape` property, which tells us the number of rows and columns as a tuple.

```python
# (rows, cols)
df.shape
```

Okay, so not _that_ big, especially for DNS logs. Let's check the columns we have. We can do that with either `df.columns` or `df.info()`. I prefer the latter because it tells us the data type of each column.

```python
df.info()
```


Ah, Zeek logs. So clean. So well-named.

These can take a while to get used to. At this point, it's a good idea to check a few rows to see what these look like. `df.head()` will print the first 5 events.

```python
df.head()
```

You may notice that between `proto` and `AA` columns is an ellipses. By default, Pandas will abbreviate output to make things easier to read. This is true for both rows and columns, but sometimes that's not what we want. In this case, I really _do_ want to see all 29 columns! I'm willing to scroll to the right!

To change this, we can use [`pd.set_option()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.set_option.html) to change `display.max_columns` to a value of our choosing. Let's do that and re-run `.head()`

```python
# Increase max cols and re-run .head()
pd.set_option("display.max_columns", 30)
df.head()
```

Behold! A scrollbar! Now we can see all the columns and determine where the data of interest lives.

Looks like for this dataset, `id_origin_p`, `query`, and `answers` have the most interesting data. That'd be the requesting IP address, the DNS query, and the responses, if any.

Why don't we make our column names a little nicer? We can rename columns with the `DataFrame`'s `.rename()` method. It takes a `dict` of shape `{"current_name": "new_name"}` for every column you want to change. This is passed as the `columns` arg. And don't forget, to make it stick in our current `DataFrame`, we need to use `inplace=True`.

I like to make sure my column names are clean right at the start of any Pandas work, and I often document the column names up front as well.

```python
# Rename columns
df.rename(columns={"id_orig_h": "source_ip", "id_resp_h": "response_ip"}, inplace=True)
# Show results
df[["source_ip","response_ip"]].head()
```

### Grouping and Aggregation

Ever made a Pivot Table in Excel? Not super fun, right? Turns out Pandas has similar capabilities with just a few method invocations. Very often we will want to group our data by a field. For example, what if we wanted to see _how many_ requests each IP in our dataset generated?

Welcome to `.groupby()`.

`.groupby()` takes a field or a list of fields to group by. However, the result is a little odd because it is [`groupby` object](https://pandas.pydata.org/pandas-docs/stable/reference/groupby.html) that doesn't show tabular data yet. That's because we need to chain it with an **aggregation function**. There are many built-in functions like `.count()`, `.mean()`, and `.sum()`, just to name a few. Keep in mind of course that these are all **quantitative** functions. They have to be, because we're talking about combining multiple rows of data into a single row. The only way a computer could sensibly do so is with mathematical functions. 

Let's group by our source IP and look at the count of how many queries each source provided.

```python
# Group by source
df.groupby("source_ip").count()
```

That's a lot of noise, since Pandas ran a count on every. single. field.

If we want to clean it up, we can specify a column at the end. But while we're at it, I also like to chain `.count()` with `.sort_values()` to get a descending count. `.sort_values()` takes a `by` argument that tells it what field to sort by, and an optional `ascending` argument to toggle ascending/descending. When sorting, you want to make sure you use the field that has the count you actually want. Look closely at the table above—not every column for a given row has the same value!

```python
# Group by source, but cleaner and descending
df.groupby("source_ip").count().sort_values(by="query", ascending=False)["query"]
```

Very clean! But `groupby()` can also take a list. Let's try grouping by source IP _and_ query, then count it up. We'll use `uid` as our sort-by. We'll also just display that field for cleanliness. To make it render as a proper HTML table rather than plain text, we'll "trick" Pandas into thinking it has a list of columns by giving it a singleton list.

Oh also, since we kinda know this is going to be large, I'm going to pregame by expanding the `display.max_rows` setting.

```python
# Increase max display rows
pd.set_option("display.max_rows", 100)

# Group by source AND query, count 'em, then sort descending
df.groupby(["source_ip", "query"]).count().sort_values(by="uid", ascending=False)[["uid"]]
```

## Filtering Values

That's a lot, right? And likely it'd be more than we need, especially when reviewing DNS queries. We can filter our `DataFrame` in a lot of ways. You've already seen the `.query()` method, and there's more to it.

But there's also the column masking method. Essentially this filters the `DataFrame` by applying a **mask**—a Series of boolean values—to a `DataFrame`, and only returning rows where the Series value is `True`.

The syntax is a little funky, so let's go through it step by step.

First, let's explain the mask. We can create a mask by using a boolean expression about a Series. For example, comparing `.source_ip` to `"10.0.1.5"`:

```python
df.source_ip == "10.0.1.5"
```

What we get back is a Series containing bools! If we put this expression inside of square braces after our `DataFrame` name, we're telling Pandas to give us rows not blocked by this mask!

```python
# Mask the df and get source_ip and query cols
df[df.source_ip == "10.0.1.5"][["source_ip", "query"]]
```

### Working with Series Data

Sometimes, the data in a Series is a little...finicky. Many data types like `str` or `datetime` have methods for working with them using the mask method.

For example, what if we wanted to mask on strings ending with a certain value? Pandas has a [`.str.endswith()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.endswith.html) method that does the job, but we have to use it properly.

> Pandas, why are you like this?

I know, it's annoying. It's because we're _never working with one value at a time_. This is a fundamental shift in our thinking about data. When working with `DataFrame`s, we have to consider what we're doing across rows and columns.

In our count of queries by source, you may have noticed a bunch of `.dmevals.local` domains. These are internal. If we're looking for external DNS queries, we can safely exclude them.

But wait. We can use `.str.endswith()` to find matches, but we want the _inverse_ match! How do?

Prepending a mask expression with `~` negates it.

Let's run that mask and save this "slice" as a new `DataFrame`

```python
# Grab our external-only queries
external_queries = df[~df["query"].str.endswith(".dmevals.local")]

# Display the results
external_queries[["source_ip", "query"]]
```

So obviously there's still some noise there. We don't really need to see the `microsoft.com` queries.

We have the ability to combine masks with boolean-like operators, although they work differently than normal Python `and` and `or`. Instead, inside the square braces, we use the bitwise `&` and `|`.

Let's add a negation for ending in `microsoft.com` to our mask.

```python
# Grab our external-only queries, minus Microsoft
external_queries = df[~df["query"].str.endswith(".dmevals.local") & ~df["query"].str.endswith(".microsoft.com")]

# Display the first 20 results
external_queries[["source_ip", "query"]].head(20)
```

So there's definitely still noise in there, but it's a lot less than there was! And this is how we begin to parse our data to find exactly what we're looking for.

## Check For Understanding

Try some of these challenges to see if you've mastered grouping, aggregation, and masking!

1. What was the average response time (`.rtt`) for queries to `.microsoft.com` domains?
2. What was the least-common external query?
3. What were the top 5 queries for `10.0.1.4`?

In the next lesson, we're going to dive even deeper into Exploratory Data Analysis with some more quantitative techniques!
