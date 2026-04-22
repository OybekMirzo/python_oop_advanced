Problem 1 (Easy): Repeat Word Iterator

You are building a simple text tool. Create a class called RepeatWord that takes a word and a number n, and produces that word exactly n times when used in a for loop. Implement the iterator protocol.
1. __init__ accepts two parameters: word (a string) and n (how many times to repeat).
2. Implement __iter__ that returns self.
3. Implement __next__ that returns the word on each call, and raises StopIteration after n times.

Input
for w in RepeatWord('hello', 4):
    print(w)

Expected Output
hello
hello
hello
hello