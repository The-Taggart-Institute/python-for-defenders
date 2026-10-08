# 2-1: Markdown

Welcome to Part 2! We begin by discussing the most important part of any Jupyter Notebook: the writing.

Although we've seen Markdown in every notebook in Part 1, we haven't really dug into the how and why of using these cells in a Notebook. There's an art to it. You want to create enough context to explain what's going on in the Notebook, while still letting the output speak for itself as much as possible.

As a reminder, you can get a fast, but thorough, introduction to Markdown syntax [here](https://commonmark.org)

**Pro tip: to make the most of this Notebook, you should be double-clicking on each cell to see how it was made in Markdown!**

## Headings

Different levels of headings (h1-h6) in Markdown make more of a difference than you might think. In addition to visually organizing your Notebook for reading, it allows the generation of a **table of contents**. Look over on the left for this icon: ![tol](img/2-1_toc.png)

See that? Yeah, Jupyter automatically creates a table of contents based on headings. 

There's also another trick Jupyter can do with headings: create slides. We'll demo how that works in a later section, but it is incredibly handy for presenting data to others.

TL;DR: use headings. They may save your life!

## Images

![galactica](img/2-1_galactica.png)

<center><i>I just needed another spaceship</i></center><br>

Images can be added to Markdown cells a variety of ways: image links from the internet, local file inclusions, and even pasting from the clipboard! That last one tends to be the source of a lot of the images I use in a Notebook, like the ToC icon in the previous cell.

Although *Galactica* sure is pretty, don't overuse images in your Markdown cells. Use them where appropriate, like for flowcharts to explain a process, or instructional screenshots to help the Notebook runner understand what's taking place.

My rule of thumb is to try to minimize the amount of scrolling one has to do in a Notebook, and images take up a lot of space. So if you use them, make them worthwhile.

## Links

Although you want your readers/runners to stay on the Notebook as much as possible, often it's necessary to link to external datasources or references. You have a few choices in how to do so.

### Inline

For informal references or links to documentation to help the Notebook runner, inline links like [this](https://docs.python.org/3/library/functools.html) are just fine. Try to structure your sentence such that the words you make hyperlinks clearly indicate what the link will be. I didn't do that in the first sentence of this paragraph. But if I wanted to talk specifically about the [functools module](https://docs.python.org/3/library/functools.html) and all the cool capabilities therein, the link makes a lot more sense.

### In-Cell Footnotes

Unfortunately, although some flavors of Markdown allow for [footnotes](https://python-markdown.github.io/extensions/footnotes/) with a special syntax, Jupyter does not support this readily. It does, however, support `<sup>` tags for superscript characters.[<sup>1</sup>](http://localhost:8888/lab/tree/2-1_markdown/2-1_markdown.ipynb#Notes) You can even use the automatically generated link for a heading to send the reader to your **Notes** section when clicking on it.

### Ending Notes

Alternatively, you can add an entire Notes cell with referenced by superscript annotations. This may be more appropriate for academic writing, allowing for a proper Works Cited/Bibliography for your work. In my opinion, this format should _only_ be used for formal citations, as otherwise it completely disrupts the reading/executing flow of the Notebook. As much as possible, keep your readers' eyes on the cell in question.


### Notes

1: See?

## Admonitions

> [!WARNING]
> This is an admonition

> [!NOTE]
> So is this.

Admonitions are **not** a standard Markdown feature, but one you'll find in [Github-Flavored Markdown](https://blog.markdowntools.com/posts/markdown-admonitions-callouts-complete-guide), a common dialect. We've installed the `jupyterlab-myst` package to take advantage of it. They're handy for calling attention to important points in your document. But don't overuse them. or they lose effectiveness.

## Small Code, Big Text

That's the rule to write by when creating Jupyter Notebooks. Be detailed (but not overly verbose) in Markdown, and succinct in your code. Take advantage of modules to abstract away complex processes that the reader/programmer doesn't need to see.

In an academic Jupyter Notebook, our intention is to demonstrate method clearly and create reproducible results. But in a professional Notebook, we care much more about the latter. Explain what's happening clearly, then get it done efficiently.

That does it for this gentle introduction to Part 2. Keep these principles in mind as we continue through the course. In the next lesson, we'll go over one more Jupyter trick to make Notebooks more user friendly: Widgets
