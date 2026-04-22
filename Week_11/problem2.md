Problem 2 (Easy+): Star Pyramid Generator

You are building a display for a text-based art tool. Write a generator function called pyramid that takes a number rows and yields strings of * characters, starting from "*" and adding one more star on each row.

1. The function accepts one parameter: rows.
2. Use yield to produce a string of i stars on each step, where i goes from 1 to rows.

Input
for line in pyramid(5):
    print(line)

Expected Output
*
**
***
****
*****