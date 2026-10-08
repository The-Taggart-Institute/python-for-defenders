# 6-3: Reporting

Not everyone wants to read all your code, nor should they. But the information your Notebooks produce will be valuable to a wide range of audiences. So how to best provide the information?

Let's start by grabbing some logs. In this case, HTTP logs from Splunk's [Boss of the SOC, v1](https://github.com/splunk/botsv1). We also need to clean up the data for use in Pandas, which this will handle.

```python
import os

if not os.path.exists("./iis.json"):
    ! wget https://s3.amazonaws.com/botsdataset/botsv1/json-by-sourcetype/botsv1.iis.json.gz -O iis.json.gz
    ! gunzip iis.json.gz
    ! sed -i '1s/^/[/' iis.json
    ! sed -i 's/}$/},/' iis.json
    ! sed -i '$s/,$//' iis.json
    ! echo "]" >> iis.json
```

Now, let's make some fun charts!

```python
import pandas as pd
import json
import plotly.express as px

# Mute an annoying PerformanceWarning
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

with open("iis.json") as f:
    json_evts = [j["result"] for j in json.load(f) if "result" in j.keys()]

df = pd.DataFrame(json_evts)
```

```python
df.shape
```

```python
df.head()
```

```python
http_method = df.dropna(subset=["cs_method"]).groupby("cs_method").count().reset_index()
px.bar(http_method, x="cs_method", y="c_ip", labels={"cs_method": "HTTP Method", "c_ip": "Request count"}, title="Requests by HTTP Method", color="cs_method")
```

![](src/img/6-3_chart-1.png)

```python
# Setup datetime
df["_time"] = pd.to_datetime(df._time.str.replace("MDT", "-0700"))
```

```python
methods_by_time = df.groupby([pd.Grouper(key="_time", freq="1D"), "cs_method"]).count().reset_index()
px.bar(methods_by_time, x="_time", y="c_ip", labels={"_time": "Time", "c_ip": "Request Count", "cs_method": "HTTP Method"}, color="cs_method", title="HTTP Requests by Day")
```

![](src/img/6-3_chart-2.png)

```python
# Create time boundary
aug_10 = df[df._time.dt.day == 10]
aug_10_10m_methods = aug_10.groupby([pd.Grouper(key="_time", freq="10min"), "cs_method"]).count().reset_index()
px.bar(aug_10_10m_methods, x="_time", y="c_ip", labels={"_time": "Time", "c_ip": "Request Count", "cs_method": "HTTP Method"}, color="cs_method", title="HTTP Requests by Day")
```

![](src/img/6-3_chart-3.png)

```python
aug_10_s_ip = aug_10.groupby("c_ip").count().reset_index()
px.bar(aug_10_s_ip, x="c_ip", y="s_ip", labels={"c_ip": "Client IP", "s_ip": "Request Count"}, color="c_ip", title="8/10/16: Requests by Client IP")
```

![](src/img/6-3_chart-4.png)

Okay so we have all of this data, and maybe more. How do we report it?

`DataFrame`s have built-in `.to_csv()` and `.to_excel()`, but that's just tabular data. What about providing data to leadership?

Jupyter has the ability to export data to PDF as well. However, that's not my preference because while it works, it's not the most visually appealing.

Instead, we can export an HTML page that contains the charts, but omits the code. We're assuming here that the audience is interested in the output. If that's not so, leave the code in—although at that point they might just want the Notebook. 

To generate a code-free HTML from a Notebook, we leverage the `jupyter` command line, like so.

```python
! jupyter nbconvert --to html --no-input 6-3_reporting.ipynb
```

Refresh the file browser on the side to view the HTML.

Jupyter has a few other export options as well, including a slideshow! Click on the gear icon on the right side to find a "Slide Type" setting. This allows you to choose whether a cell is a Slide by itself, a Fragment (appears later), a Sub-Slide (drill-down), Skip (omit), or Notes. The result is a bit wonky, but handy for presenting visual data.

## Reporting Alternatives

There are two other tools I want you to be aware of for reporting. The first is [Mercury](https://runmercury.com), a comprehensive platform to turn Jupyter Notebooks into interactive applications for non-technical audiences. The second is [Marimo](https://marimo.io), an alternative to Jupyter entirely that makes the entire Notebook out of a Python file. The editing experience is similar to Jupyter, but with some important differences and creature comforts. There is also an "App Mode" that allows a clean display of data in a web interface. Marimo is also, for better or worse, deeply inegrated with AI tools.

Regardless of tool, your work in Notebooks should be presentable to audiences that don't need to care about the code. The code is for repoducibility and ediitng by the creators, but not by leadership whose decisions your analysis informs.

## The End

Aaaand...that's it!

This is the Last Notebook. You made it! Congratulations!

If you've practiced the skills and techniques in this course, you'll be ready for the Exhibition of Mastery. There's one more unit on Next Steps, then: the Exhibition!

Congratulations, and thank you for your time, attention, and support of the Taggart Institute. I hope you've found the course worthwhile.


\- Michael
