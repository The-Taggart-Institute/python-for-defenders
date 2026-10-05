# 4-1: Requests

We're about to go on a magical journey. A journey outside of space and time, into a realm I like to call…

The information superhighway.

![surfin.gif](img/surfin.gif)

Yes, we've all navigated the internet a time or two—usually with a web browser! But it turns out Python has the ability to collect information from the internet as well, and we're going to use that ability to connect our Notebooks to powerful information sources.

To do, we must harness the power of HTTP. Luckily, Python has a handy library to do so: `requests`


```python
# Import my bff, requests
import requests
```


```python
# A simple requests demo
url: str = "https://taggart-tech.com"
r = requests.get(url)
r.headers
```

Look at that! With a simple command we were able to reach out and get the headers (and more) from my website!

`requests` is incredibly powerful. With it we can submit form data, connect to APIs, and even handle JSON. It underpins most of the API-based libraries that defenders may use like [VirusTotal](https://github.com/VirusTotal/vt-py) and [Shodan](https://github.com/achillean/shodan-python).

We've already seen how to use the library to make `HTTP GET` requests. As you might imagine, this is just the tip of the iceberg. I would get real comfy with the [Requests Documentation](https://requests.readthedocs.io/en/latest/) now. I'm constantly referencing it to make sure I'm going things correctly.

For now, let's `dir` to examine a `Response` object returned by `requests.get()`.


```python
dir(r)
# => Looooong
```

Of particular interest will be the `status_code`, which will inform us whether a request was successful, and the `text`, `content`, or `json` properties, depending on the type of data returned. `text` contains `str` of the response body; `content` contains a `bytes` of the same; and if the data can be parsed as JSON, `json` already has the `dict` representation waiting for us!
