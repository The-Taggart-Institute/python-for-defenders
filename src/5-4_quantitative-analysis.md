# 5-4: Quantitative Analysis

Let's get down to business. In this lesson, we're working with an actual, factual, malware artifact. One that you'll want to be able to manipulate easily: a packet capture. The packet capture comes from [this analysis](https://tria.ge/221108-bzzf5sdacm/).

You won't always have the luxury of a PCAP, but analyzing them with Jupyter gives us superpowers.

To extract data from a PCAP in Python, we use the `scapy` library. Let's import that and pull in the packets with the built-in `rdpcap()` function.

```python
# Import Scapy stuff
from scapy.all import *
load_layer("tls")  
# Get packets
packets = rdpcap("emo.pcapng")
```

Depending on the packet type, there will be different information available. The data is separated into OSI-model layers.

Let's start by making a DataFrame of all `IP` packets to get general information about the TCP/IP conversations in the PCAP. To do so, we will use the `.getlayer()` method to retrieve the `IP` layer, and the  `.haslayer()` method to look for the `IP` layer.

```python
# IP packets
ip_packets = [p.getlayer(IP) for p in packets if p.haslayer(IP)]
```

Let's examine the first packet to see what we're dealing with.

```python
ip_packets[0]
```

Kinda hard to read at first, but the `|` separates the layers of the packet. You can see that the `IP` layer has `src`, `dst`, `sport`, `dport`, and `len` data. In the case of this packet, the next layer is the DNS application data, which will contain the DNS query, among other things.

But for now, we're just concerned with the `IP` layer. Now that we know the names of the properties, we can access them directly. Let's make a list of `dict`s with this information to produce a `DataFrame`.

```python
# Import Pandas
import pandas as pd

# Create IP data dicts
ip_data = [{"src": p.src, "dst":p.dst, "sport": p.sport, "dport": p.dport, "len": p.len} for p in ip_packets]

# Generate DataFrame
ip_df = pd.DataFrame(ip_data)
```

```python
# Review the IP DataFrame
ip_df
```

Even without the later layers, there's a lot we can do with this data. We can begin with some **research questions**.

1. What source transferred the most bytes?
2. What destination ports are in play?
3. What are the external IP addresses?

## Grouping and Slicing for Truth

Just as we've done before, we'll by grouping our data by a field—in this case `src`. But instead of `count()`, finally, we have a reason for another aggregator. We want to add up the `len` field, so `sum()` is our choice.

> [!NOTE]
> The `numeric_only` for `sum()` tells Pandas to only aggregate fields with numbers in it.

```python
# Group by src and sum up len
ip_df.groupby("src").sum(numeric_only=True).sort_values(by="len", ascending=False)[["len"]]
```

This isn't super informative. Instead, we can do a 2-dimensional group to see largest conversations.

```python
# Group by src and dst
ip_df.groupby(["src", "dst"]).sum(numeric_only=True).sort_values(by="len", ascending=False)[["len"]]
```

That's better. If we group by all 4 fields, we start to see conversation sizes. 

We'll need to expand our max rows to see them all.

```python
# Expand max rows
pd.set_option("display.max_rows", 150)

# Group by src and sum up len
ip_df.groupby(["src", "dst","sport", "dport"]).sum(numeric_only=True).sort_values(by="len", ascending=False)[["len"]]
```

Now we can see the conversations. Looks like a lot of HTTPS traffic, which is unsurprising.

It's a little messy to look at the conversations bidirectionally. If we want to see outbound communications, we can use the IP pattern to slice our dataframe to only those.

```python
# Filter for internal sources only
outbound_df = ip_df[ip_df.src.str.startswith("10.")]

# Show the outbound comms grouped by src, dst, and dport. No need for sport.
outbound_df.groupby(["src", "dst","dport"]).sum(numeric_only=True).sort_values(by="len", ascending=False)[["len"]]
```

Much cleaner, especially with only one source!

And with that, we've answered our first research questions.

## Assessing DNS Data

For our next trick, we want to extract the DNS data from our packets. We'll use the same method we did before, looking for the `DNS` layer with `.haslayer()`.

```python
# Get DNS packets only
dns_packets = [p for p in packets if p.haslayer(DNS)]
```

DNS query data is going to live in the `qd.qname` property. They're `bytes`, so a little `.decode()` is appropriate here. We can use that to build our `DataFrame`.

Let's try to do it as a one-liner this time.

```python
dns_df = pd.DataFrame([{"id": p.id, "query": p.qd.qname.decode()} for p in dns_packets])
dns_df.head()
```

Looking good! Now, let's ask some questions.

1. What were our top queries?
2. What were the oddball queries?

Those are the common questions. Don't sleep on the rare/oddball queries. That's often where you'll find evil. Never ignore the bottom of the stack.

Hopefully this is getting familiar now. We'll group by `query` and aggregate with a `count()`.

```python
# Count of each query
dns_df.groupby("query").count().sort_values(by="id", ascending=False)
```

One of those sure sticks out, doesn't it? By the way, a solid detection opportunity is for max-length DNS queries (253 chars).

But is the long DNS query actually malicious, or just weird? We can use `pydig` and `ipwhois` right from the Notebook to find out.

> [!NOTE]
> This domain originally resolved when the course was written, but no longer has any `A` or `CNAME` records! This can happen in an investigation, and you should know how to handle it.

```python
# Whois that weird domain's owner?
from ipwhois import IPWhois
import pydig
dig_res = pydig.query("footprintdns.com", "A")
```

Hmmm, something isn't working. We need to try another record type. In fact, let's try many, and stop when we get a hit. As a refresher:

### DNS Record Types

- `A`: Anchor records, straight IP
- `CNAME`: Pointers to other domains
- `MX`: Mail exchange
- `NS`: Authoritative nameservers
- `TXT`: Metadata stored in DNS

We will loop through these and then, if something is found, use that.

```python
# Define record types
record_types = ["A", "CNAME", "MX", "NS", "TXT"]

dig_res = []

for r in record_types:
    print(f"Querying {r} records")
    dig_res = pydig.query("footprintdns.com", r)
    if len(dig_res) > 0:
        break
dig_res
```

Okay, nothing but nameservers. That tells us the domain is moribund, but the registration is still active. Let's query those custom nameservers.

```python
# Query the first nameserver
ns_res = pydig.query("ns1.footprintdns.com", "A")
print(ns_res)
# Then 
who = IPWhois(ns_res[0]).lookup_rdap(depth=1)
print(who["asn_description"])
```

What da—Microsoft??

Yeah, it's some weird tracking thing they do. It looks gnarly but is in fact legitimate.

So DNS isn't telling us much, but that in itself can be a clue! If DNS shows nothing odd, then perhaps communication was done directly via IP!

## IP Analysis/Data Enrichment

Of course we have all the IP data from these communications. It'd be nice if we would add `whois` data like the above to each IP. And what if we could run each against VirusTotal for any information?

We can.

Let's start with `df_outbound`, which handily already has our external IPs for us. We just want unique IPs, so we don't need every row in that `DataFrame`. In fact, the `groupby()` will do nicely. We want the unique IPs, so we can export the index of the `groupby()`. While this will give us an `Index` object, we can get the raw values with the `.values` property.

You might notice that the result is not a `list`, but an `array`. This is an object from the `numpy` library. It has some more capabilities than a `list`, but works similarly enough for our purposes.

We're going to build a new `DataFrame` column by column, which we haven't done before. To do this it's imperative that each list or Series that we add is the same length. We'll base everything off our `outbound_ips` array.

```python
# Get just unique destination IPs. Exclude the first entry as that's our internal IP
outbound_ips = outbound_df.groupby(["dst"]).count().index.values[1:]
```

```python
# Show the IPs array
outbound_ips
```

Now that we have the IPs isolated, let's build our new `DataFrame`. We'll pass the constructor a slightly different object than before. Instead of a list of dicts, we'll pass a single dict with the key as a column name, and the value as the column values.

```python
# Begin the DataFrame with our outbound_ips
ips_df = pd.DataFrame({"ip": outbound_ips})
ips_df
```

Now, let's enrich this data with RDAP lookups.

> [!WARNING]
> You need to handle potential errors in long-running processes. It's also a good idea to specifically except `KeyboardInterrupt` during long loops. That way, the stop button always works to kill the cell.
>
> Also, when creating Series, the size **must** match the DataFrame you're adding it to. That means sometimes filling in placeholders in the event of errors. We want to account for that in our data collection.

```python
# Initialize the list of results
whois_data: list = []

for i in outbound_ips:
    print(f"Getting {i}...", end="")
    # Use whois shell command
    try:
        whois_result = IPWhois(i).lookup_rdap(depth=1)
        whois_data.append(whois_result)
        print("Done.")
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)
        # We have to put something in here so we have a placeholder for the Series
        whois_data.append({"asn_country_code": "None"})
        continue
```

```python
# Set the `whois_country` column
ips_df["whois_country"] = [w["asn_country_code"] or None for w in whois_data]
ips_df
```

Look at that! Geo data! And one distinct outlier.

But we're not done just yet. Remember back in 4-2, when we used the VirusTotal API? Let's try searching for each of these IPs and saving the data in a new column.

We'll start by importing what we need for VirusTotal.

```python
# import the VT library and dependencies
import vt
import asyncio
from getpass import getpass
```

```python
vt_api_key = getpass("VirusTotal API Key:")
```

## Merging DataFrames

Sometimes working with two DataFrames is easier than one. In this case, we're going to populate our VirusTotal data into a separate DataFrame, then merge it into the original. 

We'll start by building the new DataFrame from the `ip` column of `ips_df`.

```python
vt_data = pd.DataFrame(ips_df["ip"])
vt_data["vt_harmless"] = 0
vt_data["vt_malicious"] = 0
vt_data["vt_suspicious"] = 0
vt_data.set_index("ip", inplace=True)
```

Let's see what we made!

```python
vt_data.head()
```

See how we used `set_index()` to make the `ip` column our Index? That's going to allow us to reference rows directly by IP address. That way, we can directly set values in the columns from the VirusTotal calls. This is also why we pre-populated the columns with blank values. Now we can use those cells!

```python
for i in ips_df.ip.values:
    # Remember VirusTotal needs async!
    async with vt.Client(vt_api_key) as client:
        r = await client.get_object_async(f"/ip_addresses/{i}")
        vt_data.loc[i, "vt_harmless"] = r.last_analysis_stats["harmless"]
        vt_data.loc[i, "vt_malicious"] = r.last_analysis_stats["malicious"]
        vt_data.loc[i, "vt_suspicious"] = r.last_analysis_stats["suspicious"]
```

```python
vt_data.head()
```

Now, it's trivial to combine these two with the `.merge()` method on the `ips_df` DataFrame.

> [!NOTE]
> We *do* have to reset the index for `vt_data`. Otherwise, `ip` won't be a common column!

```python
ips_df = ips_df.merge(vt_data.reset_index())
ips_df
```

Finally, we'll sort by those 3 columns in `malicious`, `suspicious`, and `harmless` orders to see what floats to the top.

```python
ips_df.sort_values(by=["vt_malicious", "vt_suspicious", "vt_harmless"], ascending=False)
```

We now have reason to suspect that the communication with `182.162.143.56` is suspicious. We can continue our investigation with other data sources, using this as a correlation point.
