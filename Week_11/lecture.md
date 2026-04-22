Week 11 Lecture: Iterators, Generators, and Context Managers
Available from: April 20, 2026  

This lecture covers three fundamental Python concepts: iterators, generators, and context managers. While you have likely used them extensively from the very beginning—every for loop utilizes an iterator, and every with open() statement relies on a context manager—this section will explore how they actually work behind the scenes.

1. How the for Loop Actually Works
In many programming languages, a for loop is essentially a counter (e.g., i = 0, then i = 1, then i = 2). Python’s for loop, however, does not count; instead, it asks.

Imagine we have a list of names we want to loop through:

names = ['alisher', 'sevara', 'jasur']

for name in names:
    print(name)

Behind the scenes, Python doesn’t say, “give me index 0, now index 1.” Instead, it executes a specific sequence of operations. First, it asks the list for an iterator object. You can think of an iterator as a pointer that starts just before the first element. Then, Python asks that iterator for the next item, one by one.

Here is what the for loop is doing manually:

names = ['alisher', 'sevara', 'jasur']

iterator = iter(names)
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))

iter(): Asks the object to provide an iterator (something we can pull items from one by one).
next(): Asks the iterator for the next available item.
When there are no more items left, next() raises a StopIteration exception. A standard for loop catches this exception silently and stops running. Ultimately, Python’s for loop is just a convenient wrapper around the iter() and next() functions.

2. The Iterator Protocol
How can we make our own custom objects iterable? Python relies on the Iterator Protocol, which is simply a rule requiring an object to implement two magic methods:

__iter__(): Returns the iterator object itself.
__next__(): Returns the next value in the sequence, or raises StopIteration when there are no more values.
If your object implements these two methods, Python’s for loop will know exactly how to work with it.

Building a Custom Iterator
Let’s build a Countdown class that counts down from a given starting number to 1. We start by initializing an instance variable, current, to keep track of our state.

class Countdown:
    def __init__(self, start):
        self.current = start

Next, we implement the __iter__ magic method. Python calls this exactly once, when the for loop starts, essentially asking, “Who is responsible for giving me values?”

In this simple case, the object itself will act as the iterator, so we return self. (Note: You also have the option to return a completely separate helper iterator object, which is useful if you want to loop over the same data multiple times).

    def __iter__(self):
        return self

Finally, we implement the __next__ magic method. Python calls this on every single iteration of the loop. Each call must return the next value, and when we run out of values, we must raise StopIteration. We’ll stop the iteration when current is less than or equal to 0.

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
            
        value = self.current
        self.current -= 1
        return value

Here is the complete, working class:

class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

We can now use our custom class directly inside a for loop:

rocket = Countdown(5)

for number in rocket:
    print(number)

5
4
3
2
1

Writing a full class with __init__, __iter__, and __next__ requires a lot of boilerplate code for something relatively simple. Fortunately, Python provides a shorter way: generators.

3. Generators
A generator is simply a function that can pause its execution.

While a normal function runs from top to bottom and then terminates, a generator function runs, pauses, gives you a value, and then waits for you to ask for the next value. This behavior is unlocked using the yield keyword.

Let’s rewrite our countdown example as a generator function:

def countdown(start):
    current = start
    while current > 0:
        yield current
        current -= 1

Let’s test it:

for number in countdown(5):
    print(number)

5
4
3
2
1

How yield Works
The yield keyword works similarly to return by sending a value back to the caller. However, instead of destroying the function’s state, it pauses the function.

When Python sees the yield keyword inside a function, it categorizes it as a generator function. Calling this function does not actually execute the code inside it immediately; instead, it returns a generator object.

gen = countdown(5)
print(gen)  # Output: <generator object countdown at ...>

The function body only begins to execute when you start asking it for values using next():

gen = countdown(5)
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen)) # Raises StopIteration

Every time next() is called, the function resumes execution from exactly where it paused, with all of its local variables completely intact.

yield vs. return
To clearly see the difference, observe how return behaves. Once a function hits a return statement, the function terminates.

def give_numbers():
    return 1
    return 2
    return 3
    
result = give_numbers()
print(result) # Only prints 1. Code after the first return is unreachable.

If we replace return with yield, the function can provide multiple values over time:

def give_numbers():
    yield 1
    yield 2
    yield 3
    
gen = give_numbers()
print(next(gen)) # 1
print(next(gen)) # 2
print(next(gen)) # 3

4. Iterators vs. Generators
It is important to understand the relationship between iterators and generators:

An Iterator is any object that implements the Iterator Protocol (__iter__() and __next__()). It gives you manual, full control over how state is tracked (e.g., using self.current).
A Generator is a specific kind of iterator created using a function with the yield keyword. Python automatically tracks the state and preserves local variables for you.
Note: Every generator is an iterator, but not every iterator is a generator.

Similarities:

Both produce values one at a time.
Both raise StopIteration when they are exhausted.
Both can be iterated over in a for loop.
Both remember where they left off.
Both are one-use only (once you loop through them entirely, they cannot be restarted).
Differences:

Iterators are created manually using classes and magic methods.
Generators are created simply by writing functions containing yield.
Generators are a convenient shortcut; custom iterators offer explicit control.
5. Lazy Evaluation
The real power of generators isn’t just that they are shorter to write; it is lazy evaluation.

In programming, “lazy” means delaying the computation of a value until someone actually asks for it. A generator produces one item at a time, only when next() is called. Because of this, memory usage stays near zero.

The opposite of lazy is “eager.” For example, building a list of items eagerly computes and stores every single item in memory upfront.

Look at this standard list comprehension:

evens = [x * 2 for x in range(10)]

This eagerly creates all 10 values immediately and stores them in RAM.

Now imagine we needed the first 10 even numbers from a pool of a billion numbers. If we tried doing this eagerly:

evens = [x * 2 for x in range(1_000_000_000)]
first_ten = evens[:10]

Running this code would likely crash your program because Python would attempt to build a list of one billion numbers in your computer’s memory.

A generator provides an elegant, lazy solution:

def even_numbers():
    n = 0
    while True:
        yield n * 2
        n += 1

Because it is lazy, this generator can technically produce even numbers forever while using virtually zero memory.

gen = even_numbers()
print(next(gen))
print(next(gen))

Generator Expressions
You have already learned about list, dictionary, and set comprehensions. What happens if you put a comprehension inside parentheses?

It does not create a tuple comprehension. Instead, it creates a generator expression.

squares_gen = (x**2 for x in range(1_000_000))

None of these million squares are created in memory yet. They are only generated when asked for:

print(next(squares_gen))

When passing a generator expression as the only argument to a built-in function (like tuple(), sum(), max(), min(), or ''.join()), Python allows you to drop the inner parentheses entirely:

# Feeds the generator directly into the tuple() function
squares = tuple(x**2 for x in range(1_000_000))

6. Context Managers and the with Statement
We regularly use the with statement to handle files:

with open('data.txt') as f:
    content = f.read()

The primary reason we use with instead of manually opening and closing files is safety. Consider the manual approach:

f = open('data.txt')
content = f.read()
f.close()

If f.read() crashes and throws an exception, the code stops immediately, and f.close() is never reached. The file remains locked in memory.

We could fix this using a try/finally block:

f = open('data.txt')
try:
    content = f.read()
finally:
    f.close()

While this works, it is verbose and easy to forget. The with statement handles this pattern automatically. It acts as a Context Manager, setting something up at the beginning and guaranteeing cleanup at the end, no matter what happens inside the block.

7. The Context Manager Protocol
How does the with statement know what to set up and what to clean up? It relies on two magic methods: __enter__ and __exit__.

Let’s build a custom Context Manager class called Timer that measures how long a block of code takes to run.

Setup: __enter__
This method runs the moment the with block begins. Whatever __enter__ returns is what gets assigned to the variable following the as keyword.

import time

class Timer:
    def __enter__(self):
        self.start = time.time()
        print('time started...')
        return self

If we write with Timer() as t:, the variable t becomes the self object returned here.

Cleanup: __exit__
This method runs when the with block finishes. It accepts self plus three specific parameters to handle potential errors:

exc_type: The type of the exception (e.g., ValueError).
exc_val: The exception object/message itself.
exc_tb: The traceback (the chain of function calls that led to the error).
If we return True from __exit__, Python suppresses any exceptions that occurred inside the block, pretending they never happened. Usually, we don’t want this, so we return False (or don’t return anything at all, which resolves to None—a falsy value).

    def __exit__(self, exc_type, exc_val, exc_tb):
        time_taken = time.time() - self.start
        print(f'done. took {time_taken:.2f} seconds')
        return False

Let’s test our complete Timer context manager:

with Timer():
    total = sum(range(10_000_000))
    print(f'sum: {total}')

time started...
sum: 49999995000000
done. took 0.12 seconds

8. The @contextmanager Decorator
Just as generators provide a simpler way to write iterators, Python provides a shortcut for building context managers using the contextlib module.

We can rebuild our timer as a single function decorated with @contextmanager. The trick is to use the yield keyword to separate the “setup” phase from the “cleanup” phase.

from contextlib import contextmanager
import time

@contextmanager
def timer():
    start = time.time()
    print("timer started...")
    
    yield  # The body of the `with` block executes here
    
    time_taken = time.time() - start
    print(f"done. took {time_taken:.2f} seconds")

When you use this context manager:

Everything before yield acts as __enter__.
The yield pauses the function and executes the user’s with block. (If you need an as variable, you do it here: yield start).
Everything after yield acts as __exit__.
To ensure the cleanup runs even if the code inside the with block crashes, wrap the yield statement in a try/finally block:

@contextmanager
def timer():
    start = time.time()
    print("timer started...")
    try:
        yield start
    finally:
        time_taken = time.time() - start
        print(f"done. took {time_taken:.2f} seconds")