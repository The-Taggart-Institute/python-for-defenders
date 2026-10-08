# 0-2: Why Notebooks?

There are a couple questions worth answering before we get underway.

1. Do security analysts even need to learn to code?
2. Why Jupyter Notebooks as a vehicle for introducing Python?

## Do Analysts Need to Code?

Unequivocally, no they don't. One can have a perfectly successful career in cybersecurity without learning to program—especially in the age of LLMs (I said we'd *mostly* ignore them). However, adding this skill set creates a lot of possibilities for a defense team. Automation, data parsing and transformation, deep analysis, and custom tooling are some examples of why you want some programming ability amongst the analysts. You can even make the tools you already have more effective by building the missing integrations or middleware to make them interoperate. After all, you're paying for tools that have APIs, so you might as well take advantage of them.

## Why Jupyter?

For this one, we're going to rely on Donald Knuth, the grandfather of the craft who wrote the book [_The Art of Computer Programming_](https://en.wikipedia.org/wiki/The_Art_of_Computer_Programming). He literally wrote the book!

In another of his books, [_Literate Programming_](https://www-cs-faculty.stanford.edu/~knuth/lp.html), Knuth lays out a paradigm for writing software that centers other programmers, not computers, as the "audience" of written code.

In the book's introductino, he writes:

> Let us change our traditional attitude to the construction of programs. Instead of imagining that our main task is to instruct a computer what to do, let us concentrate rather on explaining to human beings what we want a computer to do.  

Of literate programmers, he writes:

> The practitioner of literate programming can be regarded as an essayist whose main concern is with exposition and excellence of style. Such an author, with thesaurus in hand, chooses the names of variables carefully and explains what each variable means. He or she strives for a program that is comprehensible because its concepts have been introduced in an order that is best for human understanding, using a mixture of formal and informal methods that reinforce each other.

As we'll see, Jupyter's structure singularly enables literate programming. By naturally embedding "cells" of executable code with rich text, a Jupyter notebook indeed puts the human audience for the code at the forefront.

For defenders, the resulting artifact can become runbook, automation, and documentation all in one. Repeated over and over again, these notebooks can become a core part of security operations—infinitely flexible, extensible, and customizable for your needs, and as well-documented as your team's ability to write them.

I think this will make more sense as we set up the working environment. Let's go do that.
