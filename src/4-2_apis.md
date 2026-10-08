# 4-2: APIs

**A**pplication **P**rogramming **I**nterfaces are ways for one piece of software to communicate with another. In our case, we are specifically referring to HTTP endpoints where we can retrieve and send data. These are often referred to as [REST APIs](https://restfulapi.net/).

The potential value of connecting our Notebooks to external data sources cannot be overstated. By leveraging the power of the interwebs, we can verify our findings, submit new intelligence, and enrich/correlate our data to tell a more complete story.

To demonstrate this power, we will play a bit with the [VirusTotal API](https://developers.virustotal.com/reference/overview). If you're not familiar with VT, it's a fantastic resources for community-submitted malware samples and indicators. It's a primary part of my workflow.

In order to do this, you will need a **VirusTotal API Key**, which means you'll need a VirusTotal account. They are free! Go get one. I'll wait.

…

Got one? Cool. Now, don't tell anyone. Not even me.

## Seeeecrets

Okay, got your API Key? Cool. One thing that we'll commonly have to do is enter secrets like API keys or passwords into a Notebook to handle authentication. This is tricky because we certainly don't want to expose those in plaintext, and we _definitely_ don't want to save them in the state of our Notebook unencrypted. What's a Jupyteer (I just made that up) to do?

The `getpass` module allows us to collect secrets in a Jupyter Notebook and use them securely. They are _not_ stored in the saved state of the Notebook, meaning this process it Git-safe!

Let's import it and play with it.

```python
from getpass import getpass
secret = getpass("Gimme a secret!")
```

Now you _can_ print that out, but don't. Just use these secrets as you need them.


## VT The Hard Way

VirusTotal does have a Python module we can use, but I want to show you how to use the REST API directly first. 

### Headers and Authentication

It is very common for REST APIs to use a HTTP header for authentication. In VT's case, the header `x-apikey` must be present and set to a valid API key. Let's set that up now (and import requests)


```python
# Import our stuff
import requests
import json
```


```python
# Set the API key and build the headers
api_key = getpass("VT API KEY")
headers = {
  "content-type": "application/json",
  "x-apikey": api_key
}
```

Now we need a sample to test. I have one for us: a sha256sum of a strange file I found on a webserver:

**SHA256:** `1c263b3f4d21039b2a89865a4ab6600f1cc034817bae6ab1f91599674e94be72`

Now let's build our API request. Luckily, the endpoint for [Files](https://developers.virustotal.com/reference/file-info) is quite simple: a `GET` request to `https://www.virustotal.com/api/v3/files/[FILE HASH]`.

With that and our header, we should be good! Let's build that with `requests` and get our data!


```python
# Build the VT Search

# How else could we get hashes? Think back to what we've done before.
search_item: str = "1c263b3f4d21039b2a89865a4ab6600f1cc034817bae6ab1f91599674e94be72"

url: str = f"https://www.virustotal.com/api/v3/files/{search_item}"

# Note the use of headers in the GET requests
# We want the JSON result
res: dict = requests.get(url, headers=headers).json()
```


The thing about VirusTotal responses is that they can be kind of enormous. Let's break this one down to see what we have.

```python
res.keys()
```

Okay, 2 keys. Not so bad right? Well…`data` is a little bigger.

```python
data: dict = res["data"]
data.keys()
```

```python
# Now let's see attributes
attributes: dict = data["attributes"]
attributes.keys()
# => Many keys
```

Obviously there's a lot to look through. It helps to know what we're after. I like `type_description`, `names` and `popular_threat_classification` for starters. These help identify what kind of a thing it probably is.


```python
# Print some basic data
print("Type Description:")
print(attributes["type_description"])
print("\nNames:")
print(attributes["names"])
print("\nPopular Threat Classification:")
print(attributes["popular_threat_classification"])
```

If you want to go a bit deeper on the results, `sandbox_verdicts` is always interesting.

```python
attributes["sandbox_verdicts"]
```

And of course if you want the whole list of detections, that'll be in `last_analysis_results`. Because the list is so huge, I might deconstruct it a little bit. Also, knowing that failed detections are `None`s, I might use that to see just the engines that did detect it.

```python
# Use a pretty complex list comprehension to get just successful detections
positive_detections: [tuple] = [(k, v["result"]) for k, v in attributes["last_analysis_results"].items() if v["result"]]
positive_detections
```

At this point, we have a pretty good idea that our hash belongs to a Linux executable that is a **Mirai** variant. If this came from a machine under our purview, we'd have cause for alarm! Or at the very least, incident response.

## VT The Easy Way

Now that we've explored using the API "raw," we can talk about using the Python module. Now, you don't _have_ to use it! If you prefer manual HTTP requests, that's fine. But the library can make some of the ergonomics a little better. Let's import it and see.

> [!NOTE]
> We're also importing `asyncio` for reasons explained shortly.

```python
# import the VT library
import vt
import asyncio
```


Many of these API libraries are built around a `Client` class, that we instantiate with our credentials. This one does too, but here we must take a quick detour into…

### Asynchronous Python

Sometimes, processes are not finished instantaneously. Network requests often take time to complete. If we hold up the works until the request is done, that is considered a **synchronous** and **blocking** operation—nothing else can happen until that procedure is finished. However, we can also write **asynchronous** or **non-blocking** code, that will come back and do a thing once the non-instant procedure is complete. 

VirusTotal's native Python library is asynchronous. That means we need to use it as such in our Notebook. Jupyter supports asynchronous code; we just need to wrap our async calls in an `async with` block. Also, we use `await` to capture the asynchronous output inside of that block. Check out Python's [asyncio documentation](https://docs.python.org/3/library/asyncio.html) for more details.

We'll define a new client in the `with` block, passing in our API key. Then we can now perform the same search we did with `requests` by specifying the path and using `get_json()` or `get_object()`. In both cases, you still need the last part of the API path.


```python
# Async time!
async with vt.Client(api_key) as client:
    r = await client.get_object_async(f"/files/{search_item}")
    print(r)
```

`r` may not look like much, but it has everything we need easily accessible. Look!


```python
r.type_description
# => ELF
```

```python
r.sandbox_verdicts
```

Handy, right? That is much easier than navigating a ton of `dict`s
