 2-2: Widgets

Notebooks are a kind of application. Granted, they don't have a traditional user interface, but in every other sense, they are an app: code repeatedly used by a person to perform a task, structured an organized for usability.

It will frequently be the case that users will have to provide variable inputs like uploaded files, text, etc. for the Notebook to run appropriately. While we _can_ use raw variable assignments or `input()` calls, we have a better way: [ipywidgets](https://github.com/jupyter-widgets/ipywidgets).

Let's get them imported.

```python
# Import widgets and give them a nice name
import ipywidgets as widgets
```

## Basic Usage

Widgets allow us to provide easy-to-use UI components in a Notebook for changing common parameters. But from a code perspective, they get a little funky. Lemme show you. We'll start by making a slider that can set an integer value.

```python
widgets.IntSlider(min=0, max=100)
```

Cool, right? But how do you actually get that value and use it? That's where it gets a little trickier. In order to access the `value` within the object created by Widget methods, we need to assign the widget to a variable. But when we do, the widget no longer actually displays. For that reason, we need to also import another function from the `IPython.display` module: `display()`.

> [!NOTE]
> Fun Fact: IPython, or Interactive Python, was Jupyter's precursor!


```python
# Import display
from IPython.display import display
```

Now that we have the `display()` function, we can both show our widget and grab the value.


```python
w = widgets.IntSlider(min=0, max=100)
display(w)
```


```python
# Print the value of the widget
print(w.value)
```

By the way, have you clicked on that sidebar next to the cell yet? With it or the `View->Collapse` options, you can hide code or outputs for a given cell. For widgets, that means you can just show the widget without having to show the code that makes it!

## Other Widgets

Let's explore some of the other widgets and how they work. This will by no means be a comprehensive review of every widget. I encourage you to review the [Widget List](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html) from the Jupyter Widgets documentation, as well as the rest of those docs. But for now, enjoy these samples!

### Progress Bar (`IntProgress` and `FloatProgress`)

The Progress Bar is a fun way to allow a user to track the status of a long-running process. This also provide an opportunity to introduce the concept of **named parameters** in functions. We've already seen `min` and `max` for the `IntSlider`. Functions can take position parameters, identified by their order in the function call, or named parameters, which can be identified by name and have default values. For `IntProgress` and `FloatProgress`, we have a number of options to set. Check them out.


```python
# Look at all the options we can set!
progress_bar = widgets.IntProgress(
    value=0,
    min=0,
    max=100,
    description='Loading:',
    bar_style='', # 'success', 'info', 'warning', 'danger' or ''
    style={'bar_color': 'magenta'},
    orientation='horizontal'
)
display(progress_bar)
```

We can use the `time.sleep()` function to simulate a process taking time, and updating the bar's status to reflect that.

```python
# Set initial value for each run of this cell
progress_bar.value = 0
progress_bar.bar_style = ""
progress_bar.description = "Loading:"

# Import our sleep() function
# sleep(n) pauses execution for n seconds
from time import sleep

# Add 10 every second until we reach 100
while progress_bar.value < 100:
    progress_bar.value += 10
    sleep(1)

# Change the style and text for the bar upon completion
progress_bar.description = "Complete!"
```

### Dropdown

When you have multiple options to choose from, you in fact have multiple widget options to choose from! One is the `Dropdown` widget. Works as you might expect:


```python
# Create the options list (can do this inline, but I like this more)
ships = ["Enterprise", "Hood", "Reliant", "Excelsior", "Grissom"]

# Create the dropdown
dropdown = widgets.Dropdown(
    options=ships,
    value='Enterprise',
    description='Select a Ship:',
    disabled=False,
    layout = {"width": "max-content"}, # For long item names,
    style={"description_width": "max-content"} # For long description labels
)
display(dropdown)
```


```python
print(f"You selected {dropdown.value}.")
```

### Buttons

Running cells is great and all, but this is the 21st century! The age of the atom! We've walked on the moon! Cars drive themselves very poorly!

Anyway, since we're in the pushbutton age, why not...push some buttons to trigger events? With the Button widget, you can connect a Button to a function you've defined. That means you can run code with a more controlled click than running cells raw.

Now, to show output from click events, we need to use another widget as well: The Output widget. Additionally, you'll notice a new syntax here: `with`. This is syntactic sugar that simplifies common open/close procedures. In this case, we use it to use the Output widget as the destination for a `print()` invocation.

Note that we have to display _both_ the Button and the Output widget for this to work! UI programming is fun, innit?


Play with this one!


```python
# Define the Output
output = widgets.Output()

# Define the button click handler.
# Note the btn argument, which the button will provide to the on_click function
def button_event(btn):
    with output:
        print("I came from a button!")

# Define the Button
button = widgets.Button(
    description="Click me",
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip="Click me",
    icon="atom", # (FontAwesome names without the `fa-` prefix)
)

# We have to display both the Button and the Output
display(button, output)


# Set the on_click _AFTER_ displaying
button.on_click(button_event)
```

## Check for Understanding

The nature of this check means we can't do an automatic test, so please do your best to complete this challenge!

### Objectives

1. Using Widgets either described here or from the Jupyter Widgets docs, create a small app that uses our Indicator module from Part 1. 
2. Allow the user to input text, then select whether it is a Domain, IPv4, or URL
3. Have a "Defang" button that returns the defanged value.

You will almost certainly have to consult the external docs to make this happen. Take your time and use this opportunity to practice with everything we've covered so far.
