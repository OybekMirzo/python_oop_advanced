Problem 3 (Medium): Bordered Section Context Manager

You are building a console reporting tool. Create a context manager class called BorderedSection that prints a decorative top border with a title when the with block starts, and a bottom border when it ends.

1. __init__ accepts one parameter: title (a string).
2. __enter__ prints "=== <title> ===" and returns self.
3. __exit__ prints "=" repeated to match the length of the top border. It should not suppress exceptions.

Input
with BorderedSection("Results"):
    print("Score: 95")
    print("Grade: A")

Expected Output
=== Results ===
Score: 95
Grade: A
===============