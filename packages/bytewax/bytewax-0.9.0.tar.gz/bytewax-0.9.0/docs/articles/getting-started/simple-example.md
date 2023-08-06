Now that we've installed bytewax, let's begin with an end-to-end example. We'll start by building out a simple dataflow that performs count of words in a file.

To begin, save a copy of this text in a file called `wordcount.txt`:

```
To be, or not to be, that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles
And by opposing end them.
```

And a copy of the code in a file called `wordcount.py`.

```python doctest:SORT_OUTPUT doctest:ELLIPSIS doctest:NORMALIZE_WHITESPACE
import re

from bytewax import Dataflow, run


def file_input():
    for line in open("wordcount.txt"):
        yield 1, line


def lower(line):
    return line.lower()


def tokenize(line):
    return re.findall(r'[^\s!,.?":;0-9]+', line)


def initial_count(word):
    return word, 1
    
    
def add(count1, count2):
    return count1 + count2


flow = Dataflow()
flow.map(lower)
flow.flat_map(tokenize)
flow.map(initial_count)
flow.reduce_epoch(add)
flow.capture()


for epoch, item in run(flow, file_input()):
    print(item)
```

## Running the example

Now that we have our program and our input, we can run our example via `python ./wordcount.py` and see the completed result:

```{testoutput}
("'tis", 1)
('a', 1)
('against', 1)
('and', 2)
...
('them', 1)
('to', 4)
('troubles', 1)
('whether', 1)
```

## Unpacking the program

Now that we've run our first bytewax program, let's walk through the components that we used. 

In a dataflow program, each step added to the flow will occur in the order that it is added. For our wordcount dataflow, we'll want the following steps:

- Take a line from the file
- Lowercase all characters in the line
- Split the line into words
- Count the occurrence of each word in the file
- Print out the result after all the lines have been processed

We'll start with how to get input we'll push through our dataflow.

### Take a line from the file

```python
def file_input():
    for line in open("wordcount.txt"):
        yield 1, line
```

To provide our program needs an **input iterator**. We've defined a [Python generator](https://docs.python.org/3/glossary.html#term-generator) that will read our input file. There are also more advanced ways to provide input, which you can read about later when we talk about [execution modes](/getting-started/execution/).

This generator yields two-tuples of `1` and a line from our file. The `1` in this example is significant, but we'll talk more about it when we discuss [epochs](/getting-started/epochs/).

Let's define the steps that we want to execute for each line of input that we receive. We will add these steps to a **dataflow object**, `bytewax.Dataflow()`.

### Lowercase all characters in the line

If you look closely at our input, we have instances of both `To` and `to`. Let's add a step to our dataflow that transforms each line into lowercase letters. At the same time, we'll introduce our first operator, [map](/operators/operators/#map).

```python
def lower(line):
    return line.lower()


flow = Dataflow()
flow.map(lower)
```

For each item that our generator produces, the map operator will use the [built-in string function `lower()`](https://docs.python.org/3.8/library/stdtypes.html#str.lower) to emit downstream a copy of the string with all characters converted to lowercase.

### Split the line into words

When our `file_input()` function is called, it will receive an entire line from our file. In order to count the words in the file, we'll need to break that line up into individual words.

Enter our `tokenize()` function, which uses a Python regular expression to split the line of input into a list of words:

```python
def tokenize(line):
    return re.findall(r'[^\s!,.?":;0-9]+', line)
```

For example,

```python
to_be = "To be, or not to be, that is the question:"
print(tokenize(to_be))
```

results in:

```{testoutput}
['To', 'be', 'or', 'not', 'to', 'be', 'that', 'is', 'the', 'question']
```

To make use of `tokenize` function, we'll use the [flat map operator](/operators/operators/#flat-map):

```python
flow.flat_map(tokenize)
```

The flat map operator defines a step which calls a function on each input item. Each word in the list we return from our function will then be emitted downstream individually.

### Build up counts

At this point in the dataflow, the items of data are the individual words.

Let's skip ahead to the second operator here, [reduce epoch](/operators/operators#reduce-epoch).

```python
def initial_count(word):
    return word, 1
    
    
def add(count1, count2):
    return count1 + count2
    

flow.map(initial_count)
flow.reduce_epoch(add)
```

Its super power is that it can repeatedly combine together items into a single, aggregate value via a reducing function. Think about it like reducing a sauce while cooking; you are boiling all of the values down to something more concentrated.

In this case, we pass it the reducing function `add()` which will sum together the counts of words so that the final aggregator value is the total.

How does reduce epoch know which items to combine? Part of its requirements are that the input items from the previous step in the dataflow are `(key, value)` two-tuples, and it will make sure that all values for a given key are passed to the reducing function, but two separate keys will never have their values mixed. Thus, if we make the word the key, we'll be able to get separate counts!

That explains the previous map step in the dataflow with `initial_count()`.

This map sets up the shape that reduce epoch needs: two-tuples where the key is the word, and the value is something we can add together. In this case, since we have a copy of a word for each instance, it represents that we should add `1` to the total count, so label that here.

The "epoch" part of reduce epoch means that we repeat the reduction in each epoch. We'll gloss over that here, but know we'll be counting all the words from the input. Epochs will be further [explained later](/getting-started/epochs/).

### Print out the counts

The last part of our dataflow program will use the [capture operator](/operators/operators#capture) to mark the output of our reduction as the dataflow's final output.

```python
flow.capture()
```

This means that whatever items are flowing through this point in the dataflow will be passed on as outp
ut. Output is routed in different ways depending on how the dataflow is run.

### Running

To run the example, we'll need to introduce one more function, `bytewax.run()`:

```python doctest:SORT_OUTPUT doctest:SORT_EXPECTED
for epoch, item in run(flow, file_input()):
    print(item)
```

When we call `run()`, our dataflow program will begin running, Bytewax will read the input items and epoch from your input generator, push the data through each step in the dataflow, and return the captured output. We then print the output of the final step.

Here is the complete output when running the example:

```{testoutput}
('opposing', 1)
('and', 2)
('of', 2)
('end', 1)
('whether', 1)
('arrows', 1)
('that', 1)
('them', 1)
('not', 1)
('by', 1)
('sea', 1)
('arms', 1)
('a', 1)
('is', 1)
('against', 1)
('to', 4)
("'tis", 1)
('nobler', 1)
('take', 1)
('question', 1)
('troubles', 1)
('or', 2)
('slings', 1)
('mind', 1)
('outrageous', 1)
('suffer', 1)
('be', 2)
('in', 1)
('the', 3)
('fortune', 1)
```

To learn more about possible modes of execution, [read our page on execution](/getting-started/execution).
