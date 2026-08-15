# 0-1: Welcome

You might be wondering why folks on the defensive side of cybersecurity need a specialized course on the Python programming language. Unfortunately, even today Python programming is not a common skill set amongst most defenders. This lack of capability means that many defensive teams are not as efficient or effective as they could be, and so I would like to share my knowledge as a Python developer and a defender to address that gap.

## Learning Objectives

At TTI, we split our learning goals into **Skills**—things you should be able to do, and **Concepts**—things you should be able to understand.

### Skills

By the end of this course, you should be able to:

- Write Python scripts and Jupyter Notebooks
- Manage Python project dependencies
- Use Python to parse and analyze data sources
- Use data science tools techniques for analysis
- Interact with remote APIs via Python
- Create dynamic reports with Python

### Concepts

By the end of this course, you should understand:

- Python syntax
- Jupyter notebook execution
- The value of literate programming
- The tool creation process in Python
- When and why to build Python tools
- How to craft useful, reusable notebooks for use in common processes

## Course Structure

Previous versions of this course were split into two parts. Part 1 was focused on Python basics, and Part 2 applied those skills to defensive operations. These two components have since been combined into one complete course of study.

Most of the course text is within the course's Jupyter notebooks. This book will provide additional context as well as the original video lessons when appropriate.

## Prerequisites

This course does not assume familiarity with programming, but if you've had any exposure to writing code at all, it will be helpful. You will require familiarity with the Linux command line. If you need to start there, we [have you covered](https://taggartinstitute.org/t/course-catalog/125/14).

Familiarity with basic networking concepts (IP addresses, subnets, etc.) will also be valuable.

## Required Materials

You'll be running Jupyter Notebooks on your local computer. That means you'll need a way to install Python and Python packages. This course uses [uv](https://docs.astral.sh/uv/) for managing Python versions and dependencies. For Windows users, I strongly recommend using [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install) as your base platform. Mac/Linux users, you can use `uv` natively or in a guest VM, but that's on you to set up.

Previous versions of the course referenced an official virtual machine. Maintenance of that VM was too burdensome and not valuable enough to continue. Between WSL and macOS being macOS, you should have what you need. Linux users, odds are you have Python installed anyway.

## About AI

"Why bother learning Python, when AI can do all of this?"

While large language models are great at creating Python syntax, they do not *understand* anything. It is still on you, the defender, to grasp the nature of a problem and design solutions. What's more, only experts in a subject area can identify when AI goes off the rails. The only way to gain true expertise in an area is **doing it yourself**. Letting the model write the code is faster (sometimes), but we're not interested in speed at the moment. We're interested in learning. If you want to truly understand this topic, I beg you: put the agents aside for this course.

With that, again, I want to welcome you to Python for Defenders. Up next, we're going to talk about why Jupyter notebooks are so cool and why we're using them in this context.
