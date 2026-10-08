# 6-1: Visualization

I bet by the end of last lesson, you were tired of looking at giant tables. Sometimes tabular representation is the right call to tell the story of your data, but other times, a picture is worth more than ten thousand table rows.

And when you have that many, it's definitely best to avoid looking at them all row-by-row. To prove that point, we're going to work a very large file of many log entries: in this case, Sysmon logs from a Conti Ransomware event. It's so big, in fact, we can't include the file in the repository. So let's download it now.

```python
# Download logs
! curl -L -o windows-sysmon.log https://media.githubusercontent.com/media/splunk/attack_data/master/datasets/malware/conti/conti-cobalt/windows-sysmon.log
```

## Parsing Sysmon Logs

There are myriad PowerShell tools that will parse Sysmon logs and allow incident responders and threat hunters to quickly, efficiently review event data. But we're not in PowerShell, are we? Unfortunately, I was unable to find anything in the Python universe to do the same.

So I wrote one.

The code in `sysmon.py` is part of my own library of tools. Feel free to read through it, modify it, and expand it! What this module does is deconstruct WinEvent XML with `BeautifulSoup` to produce `SysmonEvent` objects, each with useful properties we can access and compare.

There's also a handy `load_xml()` function that will load the raw XML directly into a list of `SysmonEvent` objects. There's another `load_evtx()` function for files in the binary EVTX format, but that's not what we have here.

This file will be our starting point for this lesson. Let's get those events!

```python
# Import Sysmon module and Pandas, because of course
import sys
sys.path.append("../lib/")
import sysmon
import pandas as pd
```

```python
# Load Sysmon Events from the `windows-sysmon.log` file.
evts = sysmon.load_xml("windows-sysmon.log")
```

If all went well, we should have a nice list of events. Before even loading this into a DataFrame, let's look at how many events we have.

```python
# len of evts
len(evts)
```

So that's…a lot. But what does one of these things look like, anyway? Let's examine one of them

```python
# Look at the first Event object
evts[0]
```

That could be clearer. What does the object contain? One easy way to find out is with the built-in `vars()` function, which will extract the attributes of an object to a `dict`.

```python
# dict-ify our evt
vars(evts[0])
```

There now, that's something. While different Event IDs will contain some different properties, each one contains:

* `user_id`
* `event_id`
* `time_created`
* `pid`

We can use `vars()` to quickly make a big ol messy DataFrame.

You might ask why we didn't do that in the first place. Sysmon Events are complicated enough that having the structure of these objects becomes more valuable in the long run. For now, let's try to make that DataFrame by giving Pandas the `vars()` result of our objects.

We're also going to drop the `soup` field because we don't need all that data, and it's gigantic.

```python
df = pd.DataFrame([vars(e) for e in evts])
# Drop the sop column because we don't need it and it's huge
df.drop("soup", axis=1, inplace=True)
```

```python
df
```

There now, a proper `DataFrame`. But that's a table and this lesson is about visualizations! What kind of visualizations can we do? What about, say, a chart of Event IDs?

Easy enough, right? Kinda!

The good news is `DataFrames` have a built-in `plot` property that exposes all kinds of graphing features. They take some getting used to though, and they also require importing the `matplotlib` library. Let's take take of that before we do anything else.

```python
# Import matplotlib
import matplotlib
```

`matplotlib` is basically an entire course, and I will not be going into every aspect of it. We'll take what we need to make basic visualizations with it.

To start, let's say we want a simple bar chart, showing the count of every Event ID. It seems simple, but remember that right now our `DataFrame` has a row for every Event. It is not yet aggregated in any meaningful way. So up first, we know we'll have to `groupby()` and, since we want _how many_ events per, we'll use `.count()` as our aggregator. We'll even sort them for ease of use.

For ease, we'll save this slice as a new variable.

```python
# Save the counts as a new slice. This is common when working with the data
# in multiple ways
event_counts = df.groupby("event_id").count().sort_values(by="pid", ascending=False)
event_counts
```

Now to move from a table to a graph. The built-in `plot.bar` will provide us a bar graph of this data!

Using the `plot` methods takes some practice. Most of the arguments it requires are named, not positional, so you need to be familiar with the spec. I always have the [documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.bar.html) open when making these.

At base, the plot needs `x` and `y` values. The `x` axis is how we're grouping our data (`event_id`) in this case, and the `y` axis is our value to measure. Since we `count()`ed everything, we want to use a column that is present on all rows. `pid` will do nicely.

Let's try just that much.

```python
event_counts.plot.bar(x="event_id", y="pid")
```

What?? What went wrong? `KeyError: 'event_id'`? How can that be?

Welcome to Pandas. Because we grouped by `event_id`, it is no longer an accessible column; it's the Index. The very thing we needed to do to shape our data removed the column we need for the chart.

But worry not, there's a solution: we can `reset_index()` to make the Index a RangeIndex once more and get our `event_ids` column back. Our data shape is the same, but now we have the column we need. One more time!

```python
# Once more, but with a reset index
event_counts.reset_index().plot.bar(x="event_id", y="pid")
```

![](img/6-1_chart-0.png)

We made a thing! It could be prettier, but it's a chart nonetheless. `matplotlib` defaults aren't too shabby. In the next lesson we'll go over some more advanced graphing libraries, but there's more we can do to make this helpful. For one thing, every chart needs a title. Also, can we do something about those axes labels? Basic middle school science stuff.

The easiest way to make these modifications is to save the chart to a variable and work with it there. You can see above the chart that this is an `AxesSubplot` object. Commonly we'll name `Axes` objects `ax`. We can actually set the title with an argument to `plot.bar()`, but the label and the legend need methods on the axes.

```python
# Safe the axes object to manipulate it
ax = event_counts.reset_index().sort_values(by="event_id").plot.bar(x="event_id", y="pid", title="Count of Event IDs")
ax.set_xlabel("Event ID")
ax.set_ylabel("Event Count")
ax.legend(["Events"])

```

![](img/6-1_chart-1.png)

Much better! Now that we have the basics down, let's split our `DataFrame` a bit more to examine our data.

## Process Executions

Event ID 1 in Sysmon is a goldmine. Let's begin investigating process executions in our logs by isolating that Event ID

```python
# Get all process execs
process_execs = df[df.event_id == 1]
# Get the shape of the new df
print(process_execs.shape)
print(process_execs.columns)
process_execs.head()
```

Awesome, 229 events to work with. How might we visualize this data?

Perhaps as a starter we can look at the `image` field for rare occurrences. This can be done in tabular as well as graphical format. Let's get both going.

```python
# Group by image
procs_by_image = process_execs.groupby("image").count().sort_values(by="pid", ascending=False)
procs_by_image
```

I love this dataset; it's so clean. Real life doesn't always work like that. But even here, we can see some sus-looking images. `beacon.exe` indeed.

Does a chart of this information help us? I don't think it's super valuable as-is, but let's make one to see it anyhow.

```python
ax = procs_by_image.reset_index().plot.bar(x="image", y="pid", title="Executions by Image")
ax.set_xlabel("Image")
ax.set_ylabel("Execution Count")
ax.legend(["Executions"])
```

![](img/6-1_chart-2.png)

Which way did you tilt your head to look at that—left or right? The answer says a lot about you!

Didn't tilt your head at all? Okay, you _psychopath_.

But seriously, this isn't a great way to display this data. In the case of process executions, a table is better. Why did we do this at all then? To drive home this point:

**Use the right form to tell your data's story**. Tables aren't always correct and neither are charts.

## Network Connections

This one is going to lend itself much better to visualization. Event ID 3 shows network connections, and has source, destination, and port information in there. Let's grab 'em.

We'll also just print out the columns we care about.

```python
# A new slice for EventID 3
network_conns = df[df.event_id == 3]
print(network_conns.shape)
print(network_conns.columns)
network_conns[["time_created","pid","image","user","src_ip","dest_ip","src_port","dest_port"]].head()
```

### Ports

Let's see what ports were most used by grouping and graphing. We're going to do this all in one move. The line of code gets long, but we can split it with ` \` characters.

Oh one other trick. We are going to only take the **top 10** entries with a creative sort. Why? Because without that, the number of ports would make this utterly unreadable.

```python
# Group and graph
ax = network_conns \
  .groupby("dest_port") \
  .count() \
  .reset_index() \
  .sort_values(by="pid", ascending=False) \
  .head(10) \
  .plot.bar(x="dest_port", y="pid", title="Network Connections by Destination Port")

ax.set_xlabel("Dest Port")
ax.set_ylabel("Conn. Count")
ax.legend(["Connections"])
```

![](img/6-1_chart-3.png)

Now that we have an overview, we can dive in on the points of interest in the dataset.

## Zooming In on Processes of Interest

Now we see some interesting processes right? `beacon.exe` in particular. We can do some really interesting graphing/tabling with that information.

Let's isolate that in a new slice and see what kind of events it emits. We'll do so with the `image` and `parent_image` properties, looking for what the process did, but also anything its immediate child processes did. Then we'll graph the events.

```python
# Slice for beacon or beacon's kids
beacon_exe = df[df.image.str.endswith("beacon.exe") | df.parent_image.str.endswith("beacon.exe")]
# Graph Events
ax = beacon_exe.groupby("event_id").count().reset_index().plot.bar(x="event_id", y="pid", title="Beacon.exe Event IDs")
ax.set_xlabel("Event ID")
ax.set_ylabel("Event Count")
ax.legend(["Events"])
```

![](img/6-1_chart-4.png)

So a few process execs, a lot of network activity, some file writes? and a massive amount of registry activity. That's not exactly uncommon, but worth noting.

It's important to see that there are in fact network connections. To what?

```python
# Beacon Network Connections
ax = beacon_exe[beacon_exe.event_id == 3] \
  .groupby("dest_ip") \
  .count() \
  .reset_index() \
  .plot(kind="bar", x="dest_ip", y="pid", title="Beacon.exe Destination IPs")
ax.set_xlabel("Dest IP")
ax.set_ylabel("Conn. Count")
ax.legend(["Beacon.exe"])
```

![](img/6-1_chart-5.png)

```python
ax = beacon_exe[beacon_exe.event_id == 3] \
  .groupby("dest_port") \
  .count() \
  .reset_index() \
  .plot(kind="bar", x="dest_port", y="pid", title="Beacon.exe Destination ports")
ax.set_xlabel("Dest Port")
ax.set_ylabel("Conn. Count")
ax.legend(["Beacon.exe"])
```

![](img/6-1_chart-6.png)

Mostly on 443. Unsurprising, but that does mean we may have one other bit of data to grab: DNS, aka Event ID 22.

I think this may be nicer as a table.

```python
# Check out event ID 22
beacon_exe[beacon_exe.event_id == 22][["time_created","query_name","query_results"]]
```

Well hello there. Here we have a C2 calling home to multiple subdomains, but all resolving to the same IP.

There's plenty of other investigation we can undertake with this sample, but much of it may require a bit more complex visualization. That's why we're going to stop here for this lesson. 

Take some time to practice with `df.plot`. Try other chart types! Try stacked plots! 

In the next lesson, we'll explore more complex visualization libraries. See you there!

