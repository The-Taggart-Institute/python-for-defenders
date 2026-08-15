## 0-2: Why Notebooks

Do security analysts need to code? The answer has never been more complicated. 

before we get into the main material i
think we need to answer a couple of
questions
first of all why are we going to use
jupyter notebooks and actually
before we even get there
do analysts need to code does the
defensive team need to be made of
programmers the answer is an unequivocal
no you can have a perfectly successful
career
as a security analyst even as an
incident responder without learning to
program however
with this additional skill set a lot of
possibilities open up for the team
automated common procedures you can
parse data more efficiently and more
effectively
you can use the tools that you have at
your disposal that you pay for in a
deeper way by taking advantage of their
apis and writing your own integrations
to them
you can even rely less on other teams
and on vendors and maintain
a lot of the expertise necessary to do
what you do inside of the security
operations team so while it is possible
for a defensive team whether it's
incident responders whether it's the
analysis team even whether it's the
engineers
to have a successful career without
learning to code
by adding this skill set it really is a
tremendous force multiplier so why are
we doing all of this inside of the
context of jupyter notebooks i know this
is a wall of text i'm going to read it
out for you anyway
what we're after here is a concept known
as literate programming which was
coined
by donald knuth who literally wrote the
book the art of computer programming he
is one of the grand masters of the art
and in his book literate programming he
talks about the concept
that we're enacting here
in the introduction he says let us
change our traditional attitude to the
construction of programs instead of
imagining that our main task is to
instruct a computer what to do let us
concentrate rather on explaining to
human beings what we want a computer to
do
he says of literate programmers the
practitioner of literate programming can
be regarded as an essayist whose main
concern is with exposition and
excellence of style such an author with
thesaurus in hand chooses the names of
variables carefully and explains what
each variable means he or she strives
for a program that is comprehensible
because its concepts have been
introduced in an order that is best for
human understanding using a mixture of
formal and informal methods that
reinforce each other
basically
rather than thinking of the machine as
the primary audience for what we're
writing
in terms of code we're going to think of
the human who has to read the code as
the primary audience
this is possible with jupiter for a
couple of different reasons but
importantly the structure of jupiter
notebooks co-mingles text that is human
readable and python code or other kinds
of code actually but for our purposes
python that is interpreted by the
computer
the result
for defenders and other people who use
jupyter notebooks like data scientists
is that the procedure the tool and the
actual steps you have to take in order
to complete a process and the
documentation are the exact same thing
think of this as a self-documenting
program or a self-documenting script
every step can be explained as it occurs
you can then take these self-documenting
programs and host them on shared
resources that the entire team can use
and then they can easily be updated and
expanded as needs change
so that's the why and wherefore of what
we're trying to do with python and
specifically python in the context of
jupiter i think this will make more
sense as we actually dive in so let's
get started with that up next we're
going to set up our environment for
jupiter
