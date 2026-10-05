# 3-5: LAB | IoC Extractor

It's time to build a real tool with all we've learned! We're going to solve a GIANT problem defenders face constantly: extracting indicators from garbage source files.

Sometimes, indicators are received in mixed formats. MD5 hashes, SHA1s, SHA256s, IPs, domains, and URLs are all jumbled together.

Sometimes, some sadistic monster decides to provide all of these in a PDF for no reason other than to make us suffer.

But that ends now.

Our IoC extractor will take any text file, find all the strings matching our indicator patterns, and produce either a CSV or JSON for easy ingestion into our defensive tools.

We'll build it using widgets to make it easy to work with.

Let's import what we'll need.

**NOTE: We're gonna use a new library, `pdfplumber`, to handle PDFs. Don't worry; we'll cover it when it comes up.**


```python
# Get our gear
import ipywidgets as widgets
from IPython.display import display
import json
import csv
import pdfplumber
import re
```

## Step 1: Acquire Files

First we need the files. Let's get 'em, widget-style!


```python
# Define and display widgets
upload = widgets.FileUpload(multiple=True, accept=".csv, .txt, .json, .pdf, .html")
label = widgets.Label(value="Upload File(s)")
box = widgets.HBox([label, upload])
display(box)

```

## Step 2: Extract Raw Content

Something kind of counterintuitive about this process is that, with the exception of PDFs, we don't really care about what kind of file it us. We just want the raw text, because we'll be doing our own parsing of the content to look for our patterns. PDFs present a special challenge because they are not plain text; they are binary blobs. That's why we imported the `pdfplumber` module to help us out.

Let's briefly discuss how to use `pdfplumber`.

### `pdfplumber`

Since PDFs are binary blobs, we can't just do `with...open...readlines()`. But that's okay; the plumber has us covered. `pdfplumber.open()` takes a path and returns a `PDF` object. This object in turn contains a `pages` property that holds a bunch of `Page` objects. FINALLY, those `Page` objects have an `.extract_text()` method that will stringify the contents of the page! Check it out.


```python
# Extract text
with pdfplumber.open("esxi_mandiant.pdf") as pdf:
  text_pages = [p.extract_text() for p in pdf.pages]
  
# Review page 1
text_pages[0]
```

Okay, so we plainly have a way to handle PDFs. Now we need the entire procedure for handling all our files. If it's plaintext, we can just grab it from the widget. But if it's binary, we'd be better off using `pdfplumber`. My first move would be to define some functions.


```python
# First our PDF extractor
def get_pdf_text(pdf_path: str) -> str:
  """
  Extracts text from file at pdf_path and returns a big ol' string of the results
  """
  with pdfplumber.open(pdf_path) as pdf:
    return "".join([p.extract_text() for p in pdf.pages])
  
def get_file_contents(index: int, uploads: tuple) -> str:
  """
  Seeks the upload widget value for a given filename.
  
  If it's there and it's not a PDF, grabs the content as a string.
  
  PDFs, it will use the filename with get_pdf_text
  """
  # Check for a PDF
  if uploads[index]["type"] == "application/pdf":
    return get_pdf_text(uploads[index]["name"])
  
  # Otherwise, get the contents
  return bytes(uploads[index]["content"]).decode()
  
```

Okay! Functions in hand, we can go get our data. We'll keep everything in a `dict` so we'll once again use that `dict` comprehension trick we saw before.

```python
# Get data
data: dict = {f['name']: get_file_contents(i, upload.value) for i, f in enumerate(upload.value)}
```

You can look at `data` if you want, but it's gonna be a hot mess so I'm leaving it alone for right now.

## Step 3: Match Patterns

Data in hand, we need some ✨regular expressions✨ to match our patterns. What do our indicators look like? Luckily, our hashes have known lengths and URLs/domains/IPs are fairly simple.

* `MD5`: 32 characters of lower case 0-9,a-f
* `SHA1`: 40 characters of the same
* `SHA256`: 64 ""
* `SHA512`: 128 ""
* `IPv4`: 1-3 digits and a dot, repeated 3 times, followed by 1-3 more digits
* `domain`: A-Z,a-z,0-9,- separated by dots, ending in 2-n a-z characters
* `URL`: `http`, maybe `s` `://`, a domain pattern, and any number of `/` followed by the same characters allowed in domains,plus`%`,`?`,`=`,`&`, and `+`.

Now, we do have an extra complication here: overlaps. A SHA512 will contain 4 MD5 pattern matches! How do we avoid this issue? Negative lookarounds. We will use the `(?<![0-9a-f])` and `(?![0-9a-f])` patterns to discard matches with hex characters immediately before or after the smaller matches. This is some advanced regexery, but it's what we need here.

It's Regex time!


```python
# Define our regexes
# Yes, I'm giving these to you. Feel free to improve on them!
md5_pattern = re.compile(r"(?<![0-9a-f])[0-9a-f]{32}(?![0-9a-f])")
sha1_pattern = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
sha256_pattern = re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")
sha512_pattern = re.compile(r"[0-9a-f]{128}")
ipv4_pattern = re.compile(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}")
domain_pattern = re.compile(r"(?:[A-Za-z0-9\-]+\.)+[A-Za-z]{2,}")
url_pattern = re.compile(r"https?://(?:[A-Za-z0-9\-]+\.)+[A-Za-z0-9]{2,}(?::\d{1,5})?[/A-Za-z0-9\-%?=\+\.]+")
```


Yeesh. With those in hand, it's time to parse our data. Again, we're building a `dict` whose keys are our filenames. Inside each is a `dict` whose keys are our match types. Easiest way here is with a loop.

You might notice an unfamiliar bit of syntax in those regexes: `(?:...)`. These are _non-capturing groups_ which are necessary to prevent `.findall()` from returning just that group.

Oh, one other thing. It's likely that a given file will have repeated indicators. We need an easy way to deduplicate our findings. We could write an algorithm to check and remove duplicates, but there's an easier way.

The [`set`](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset) data type is a sequence that enforces uniqueness. Converting a list to a set automatically deduplicates the elements. Sets are immutable, so we lose some flexibility, but they're fantastic for this exact use case.

But, because we can't save `set`s as JSON, we're going to immediately convert them back to `list`s. This is the kind of nonsense that you'll see often in my code, and it's a symptom of training as a functional programmer. There are a lot of parentheses.



```python
# Initialize an empty dict
results = {}

# Loop through our strings
# Convert our findings to sets to deduplicate
for d in data:
  content = data[d]
  results[d] = {
    "md5": list(set(md5_pattern.findall(content))),
    "sha1": list(set(sha1_pattern.findall(content))),
    "sha256": list(set(sha256_pattern.findall(content))),
    "sha512": list(set(sha512_pattern.findall(content))),
    "ipv4": list(set(ipv4_pattern.findall(content))),
    "domain": list(set(domain_pattern.findall(content))),
    "url": list(set(url_pattern.findall(content))),
  }
results
```

Okay, so is it perfect? No. It turns out files with extensions are basically indistinguishable from domains. But otherwise, pretty solid! Let's take this and deliver our results. To do so, we'll offer 2 buttons: a CSV export, and a JSON export.

Buttons are event-driven, so we also need to first write the functions that will perform the export.


## Step 4: Deliver Results

Reshaping our data into JSON format is essentially done for us. But flattening it out into a CSV, well, that's gonna be a little trickier.

If we imagine our CSV with 3 columns, like so:

**Filename** | **IOC Type** | **Value**
--|--|--
Foo.txt | domain | evil.com

We can see that a bit of destructuring is necessary.

For now, rather than be super elegant with it, we'll be clear. Sadly, this means it'll involve 2 nested loops (gross) and a list comprehension. So really 3 nested loops, but one is prettier.


```python
# Give an output
output = widgets.Output()
# Create the buttons.
json_button = widgets.Button(description="JSON Export")
csv_button = widgets.Button(description="CSV Export")

# Provide an output display
box = widgets.HBox([csv_button, json_button, output])
display(box)

# Define filenames
CSV_RESULTS: str = "results.csv"
JSON_RESULTS: str = "results.json"

# Create the export handlers
def csv_export(b):
  
  with output:
    header = ["filename", "type","value"]
  with open(CSV_RESULTS, "w") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for filename in results:
      # Add filename to the the dict
      result = results[filename]
      for ioc_type in result:                    
        iocs = result[ioc_type]
        rows = [[filename, ioc_type, i] for i in iocs]
        writer.writerows(rows)
                
    # Notify when done
    print(f"{CSV_RESULTS} written")
      
def json_export(b):
  
  with output:
    with open(JSON_RESULTS, "w") as f:
      json.dump(results, f)
      print(f"{JSON_RESULTS} written")


csv_button.on_click(csv_export)
json_button.on_click(json_export)

```

## Step 5: Celebrate!

That's it! We now have a take-all-files IoC extractor. Remember that this file is meant to explain the lab, but that you should try to reproduce it in your own Notebook to understand in depth how each piece works.

At long last, we're finished with our unit on Parsing. Up next, we move off our one computer and use Jupyter to connect to resources on the internet!

## References

1. Mandiant, 29 September 2022. ["Bad VIB(E)s Part One: Investigating Novel Malware Persistence Within ESXi Hypervisors"](https://www.mandiant.com/resources/blog/esxi-hypervisors-malware-persistence)
2. AlienVault, 12 September 2022. ["HEINEKEN Malaysia 'Free Beer' phishing scam circulating through social networks which has been detected by NetAssist Threat Intelligence team"](https://otx.alienvault.com/pulse/632025d828a36b7ea31c11fa)
3. CISA, 30 June 2022. ["#StopRansomware: MedusaLocker"](https://www.cisa.gov/uscert/ncas/alerts/aa22-181a)

