# 5-1: Pandas

No, not the useless overgrown rodents. [Pandas](https://pandas.pydata.org/) is an incredibly powerful data science library that allows deep statistical analysis on datasets through an easy-to-use API.

The simplest way I can explain it is this: imagine if Excel had a command line interface.

## Tabular Data

The reason I chose Excel as our metaphor is that Pandas deals with **tabular data**—data represented in rows and columns, like a spreadsheet. It comes packed with tools to parse, filter, summarize, and analyze these rows and columns, far beyond what would be easily accomplishable in a GUI.

To get started, we will need ourselves a dataset. Let's take this opportunity to solve another common problem in defense: rapid IP/domain name lookups.

## Looking up IP/Domain data

Very often, I will need to pull DNS records for a suspicious domain, then immediately pivot on that IP address to a RDAP/whois lookup on that IP address from [ARIN](https://www.arin.net) data. I've gotten pretty quick at doing this on the command line, but especially if I have ot do it for multiple domains/IPs at once, it is nice to have a tool that automates the retrieval, and tabulates the data for me for simple review.

For this, we will leverage three different Python modules: `pydig`, `ipwhois`, and `geoip2fast`. `pydig` gets us domain → IP conversion; `ipwhois` looks up the ARIN data; and `geoip2fast` enriches that data with more accurate geographic locations for subnet. 

Our procedure will look like so:

1. Create the list of IPs/Domains to review
2. For each entry, do the following:
   1. If it's a domain name, look up the IP via `dig`.
   2. With the IP, perform an [RDAP](https://about.rdap.org) lookup on the IP
   3. Collect CIDR, AS name, number, and listed location.

Our final `dict` for each domain/IP will look like:

```
{
    ip: str
    domain: str
    asn: int
    as_name: str
    cidr: str
    country: str
    city: str
}
```

Let's build our list of domains and then set up the information collection.


```python
# Import our stuff
# Pandas is conventionally named pd
import pandas as pd
import pydig
from ipwhois import IPWhois
from geoip2fast import GeoIP2Fast
from ipaddress import IPv4Address
```

We need to use `geoip2fast`'s command line to update its local database. You can do this directly in Bash or in the Jupyter Notebook with:

```python
# We also need to use the geoip2fast command line to install its database
# Omit the ! for direct Bash usage
! geoip2fast --update-all
```

I'll use the list of sites from the last lesson, but feel free to modify it! It won't affect the run of this Notebook.

```python
# Our sites to analyze
sites = [
  "taggart-tech.com",
  "npr.org",
  "penny-arcade.com",
  "tomshardware.com",
  "meta.com",
  "cnn.com"
]
```

### Putting the Data Together

Handling all these API calls and compiling the data is a tricky feat. First, we have to handle the possibility that the type of DNS record we're looking for isn't what a given domain name resolves to. `A` records will return IP addresses, but `CNAME`s will return other domains. We have to handle that. We'll do a best effort depth-1 resolution of `CNAME`s to IPs by catching the first error and retrying for `CNAME` records, then querying *that* for an `A` record.

And if even that doesn't work, we'll fail over to blank ASN data. By the time we get to building the `dict`, we should have all the errors handled.

> [!TIP]
> This is a straight script, but perhaps you can think about how to build it as a function?


```python
# Initialize sites_data to an empty list
sites_data = []

# Initialize the GeoIPFast client
gip = GeoIP2Fast()

for s in sites:
  try:
    dig_res = pydig.query(s, "A") # Querying A records for IP addresses
  except ValueError:
    # If no A records, look for CNAME
    cname_res = pydig.query(s, "CNAME")
    dig_res = pydig.query(cname_res[0], "A")
  resolution = dig_res[0]
  try: 
    addr = IPv4Address(resolution)
    whois_target = ipwhois.IPWhois(resolution) # We'll get the first result
    whois_res = whois_target.lookup_rdap(depth=1)
  except:
    # We create a mock whois_res to satisfy object creation
    whois_res = {"asn": None, "asn_description": None, "asn_cidr": None}
  
  gip_res = gip.lookup(resolution)
  sites_data.append({
    "resolution": resolution,
    "domain": s,
    "asn": whois_res["asn"],
    "as_name": whois_res["asn_description"],
    "cidr": whois_res["asn_cidr"],
    "country": gip_res.country_code,
    "city": gip_res.city.name
  })
```

Phew! And after all that, what does our data look like?



```python
sites_data
```

Well that's readable, but not very. But the way we created this dataset is intentional. Every `dict` has the same keys and value types, which means it is really easy for us to create a **Pandas DataFrame** from it. This will produce a data structure that is not only easy to work with, but displays cleanly in Jupyter.

Let's make a new DataFrame from `sites_data`. By convention, primary DataFrame variables are named `df`.

```python
# Create our new DataFrame
df = pd.DataFrame(sites_data)
```

## Exploring DataFrames

DataFrames are a deep topic, and this lesson (and the next) really won't cover more than a small fraction of what's possible. If you want to become extremely fluent in DataFrame usage, I encourage you to spend some time reading the [Pandas documentation](https://pandas.pydata.org/docs/).

But we can still learn some basics. Let's preview our data with the `.head()` method, which show the top 5 (by default) values from the DataFrame.


```python
# Look at the top of it with the built-in `.head()` method
df.head()
```

Looks great, right? In addition to a clean table display, the DataFrame API is *powerful*. Let's play a little bit with it. Let's select just two columns: `as_name` and `cidr`.

> [!NOTE]
> Pandas syntax looks pretty strange at first, but you'll get used to it. Here we're providing the column names as a list to the DataFrame in index notation.

```python
df[["as_name", "cidr"]]
```

We can also use the `.query()` method to write structured queries against the data. Let's look for `Fastly` in the `as_name`.

```python
df[df.as_name.str.contains("FASTLY")]
```

There is so much to explore in DataFrames, and we're going to dive in for real in the next lesson. This was meant as a quick intro to the concept of using Pandas and how to consider shaping our data to be useful in tables. 

See you in the next lesson where we'll get serious about Pandas! But before we get out of here, I'll leave you with probably the most import Pandas feature: `.to_csv()`

```python
df.to_csv("sites_data.csv")
```
