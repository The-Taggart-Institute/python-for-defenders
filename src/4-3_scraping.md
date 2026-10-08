# 4-3: Scraping

APIs are great, but they can't do everything. Sometimes we need to use other methods to analyze content. Specifically, I want to discuss how we analyze web content either for disposition or to extract useful information from it. Put another way, how can we make Python read and understand websites programmatically?

The answer is BeautifulSoup.

## Funny Name, Invaluable Library

This may be one of the most important Python modules I've ever used. [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) is a parser for HTML/XML files. With it, we can do some pretty incredible things. Let's start by learning the basic shape of BS4.

We begin by importing the library

```python
# import and setup
import requests
from bs4 import BeautifulSoup
```

Now we need to give it something to parse. Once again, My simple blog serves well for this.

```python
document: str = requests.get("https://taggart-tech.com").text
```

```python
soup = BeautifulSoup(document)
```

`soup` is a complex object, but it helps us parse the HTML in valuable ways. Let's grab the page title as an example.


```python
# Access the title
soup.title
```

At first glance, that might seem like a string of HTML. But look carefully: no quotes. No, this is something else.


```python
# What are you, soup.title?
type(soup.title)
```

As a `Tag` object, there's more we can do with the title. Including extract its text.

```python
soup.title.text
```

Now _that's_ a string.


## Seeking through HTML

The power of BeautifulSoup comes from the ability to slice through a document for exactly what we want. For example, say we watned to pull all the links (`<a>`) tags out of the page. We could use the `.find_all()` method to do just that.


```python
# Grab links
links = soup.find_all("a")
# Show the first one
links[0]
```

Again, since the results are `Tag` objects, we can destructure this a little bit more to access just the `href` attribute.

```python
# Get just the hrefs 
# And use (set) to dedup
hrefs = set([ l["href"] for l in links ])
hrefs
```

The syntax of all the ways to work with BeautifulSoup objects can be a bit confusing. I almost always have the [documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) up while I'm working with it. Still, the capabilities are quite impressive.

## An RSS Reader?! Yes.

We can heal the wounds. We can create an RSS Feed processor in Python. 

Did you know CISA's [US-CERT](https://www.cisa.gov/uscert/ncas) has an RSS Feed? It's true! It's a solid way to get basic information about emerging threats.

So let's build handler and parser to:

1. Process the Feed
2. Produce Headlines
3. Get data from linked articles.

To start, let's set up the URL of the RSS feed:


```python
# Set feed URL
feed_url: str = "https://www.cisa.gov/uscert/ncas/current-activity.xml"
```

Then we'll download the data with `requests` and use BeautifulSoup to parse the XML.

```python
# Get the XML
us_cert_xml = requests.get(feed_url).text
```

```python
# Soupify the XML

soup = BeautifulSoup(us_cert_xml, "xml")
```

Now that we have the parsed XML, we need to understand the structure. Every article is inside of an `<item>` tag. So to get all the items, we will use the `.find_all()` method.


```python
# Get all <item>s
items = soup.find_all("item")

# Review one for structure
items[0]
```

So each `item` has a `title`, a `link`, and a `description`. That's enough to get us going. But how should we handle it?

One option might be the `HTML` Widget. We can convert each item into some crafted HTML.

Did you notice the weird characters in `description`? The HTML tags have been escaped to make them XML safe. To reverse that, we'll need the `html.unescape()` method. A simple import, but worth mentioning. 

Okay, let's write a function to HTMLify the items.


```python
from html import unescape

def html_item(item) -> str:
  """
  Converts an XML item into HTML
  """
  item_html = f"<a href=\"{item.link.text}\"><h2>{item.title.text}</h2></a>"
  item_html += f"<p>{unescape(item.description.text)}</p>"
  return item_html
```


And now, to display the results. I'm adding a little `<style>` to the proceedings to make the links pop.



```python
import ipywidgets as widgets
from IPython.display import display

style_html = """
<style>
  a {
    color: #9580ff;
    font-weight: boldest;
  }
</style>
"""

# We'll just do the first 3 items 
html_items = [ html_item(i) for i in items[:3] ]
html_str = "".join(html_items)

html_out = widgets.HTML(value=style_html + html_str)
display(html_out)
```

Now this is one way to parse and use this data, but I'm sure you can come up with others—and other feeds to connect to. Get creative!

In our final lesson in this section, we'll build a webpage analyzer to assess for potential malware!
