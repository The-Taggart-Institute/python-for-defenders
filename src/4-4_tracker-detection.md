# 4-4: Tracker Detection

It isn't all about malware, you know.

Being able to safely determine what a website does without using a browser is a common function of a defense team. Of particular interest is any tracking technologies in use by a site. You may have seen some recent news regarding one of the most insidious: the [Meta Pixel](https://developers.facebook.com/docs/meta-pixel/)
Another common tracker is, of course, [Google Analytics](https://analytics.google.com/). 

If we want to identify whether a site is using these, we can use our parsing powers to do just that.

We'll start by importing the stuff we know we'll need.

```python
# Import the basics
from bs4 import BeautifulSoup
import requests
import re
```

## Recon

First, we need to know a little about what we're trying to identify. These trackers will have identifiable code snippets in page we analyze. For flexibility, we'll store these patterns in a `dict`. You can learn about the code that makes these trackers up in their documentation. For both Meta and Google, we're talking about JavaScript.

Meta uses a script with the obvious pattern of a URL: `https://connect.facebook.net/en_US/fbevents.js`. Google uses a URL as well, but as a `src` attribute for its script. Another pattern we can use in the text of a script node is `gtag('config'`.

So let's store those for later reference.


```python
# Set up patterns
# Using a raw string to escape the paren
script_patterns = {
  "meta": "https://connect.facebook.net/en_US/fbevents.js",
  "google": r"gtag\('config'",
  "plausible": "plausible.init"
}
```

Now we need a list of pages to search. You can add whatever pages you like to this list, but I'll kick it off with a few.


```python
# Build the list of sites
sites = [
  "taggart-tech.com",
  "npr.org",
  "penny-arcade.com",
  "tomshardware.com",
  "meta.com",
  "cnn.com"
]
```

Our results will be stored in a `dict` as well. For each site, we need to:

1. Pull the web content
2. Find all `script` tags
3. Check if any of them match our patterns 
4. Report results

A few key words in these steps give us hints about how to proceed. `any()` is a built-in. Python function that take 2 arguments: a function, and a sequence over which to iterate the function. The function must return a `bool`. If any of the elements return `True` when passed to the function, `any()` returns `True`. There's also an `all()` that works similarly, but `any()` will work for our purposes. So let's write the `pattern_match()` function.


```python
def pattern_match(pattern: str, sample: str) -> bool:
  """
  Checks whether a pattern is found in a sample
  """
  return re.search(pattern, sample) != None
```

It isn't much, but it will provide what we need to pass to `any()`...sorta.

But first, let's initialize our results `dict`. The shape will be `{site: [tracker names]}`.

```python
results = {}
```

So now we need to loop through our sites, grab the `script` elements, and check for patterns with `any()`. The idea here is that if any of the `script` elements match our pattern, we know we have the given tracker.

This is one of those instances where a `for` loop is absolutely more appropriate than a list comprehension for readability and maintainability.


```python
# Loop through sites
for s in sites:
  # Initialize site list
  results[s] = []
  print(f"Fetching {s}")
  # Get content
  content: str = requests.get(f"https://{s}").text
  soup = BeautifulSoup(content)
  # Find script tags
  # Extract just the text to get the raw str
  script_tags = [ t.text for t in soup.find_all("script") ]
  # Loop through patterns to check
  for p in script_patterns:
    pattern: str = script_patterns[p]
    # Check if any of the scripts have the pattern
    if any([pattern_match(pattern, t) for t in script_tags]):
      results[s].append(p)
```

```python
# Show results
results
```

> [!NOTE]
> Change the sites up for different results!

## Going Further

One of my favorite tools for web app testing is [Wappalyzer](https://www.wappalyzer.com/), which will detect technologies in use on a page via server headers and source analysis. We're going a simplistic version of this here, but wouldn't you know it: Wappalyzer has a [Python module](https://pypi.org/project/python-Wappalyzer/)!

Because I'm cool like that, I've already added it as a dependency in this environment. See if you can rework this lab using Wappalyzer to detect WordPress sites or other technology!

And that closes out section 4! Up next, we begin to analyze our data with scientific tools!
