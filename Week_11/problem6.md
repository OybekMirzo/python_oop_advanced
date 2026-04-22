Problem 6 (Advanced+): Cash Register with Generator-Powered Context Manager

You are building a point-of-sale system. Create a context manager class CashRegister that internally uses a generator with send() to track a running total. When the with block ends, it prints a full transaction report.

1. __init__ accepts one parameter: name (register label).
2. Create a protected generator method _accumulator that starts a running total at 0. In an infinite loop it receives a value via yield, adds it to the total, and yields the new total.
3. __enter__ creates the generator, starts it with next(), initializes an empty history list, and returns self.
4. Implement an add(amount) method that calls send(amount) on the generator and appends a tuple (amount, running_total) to the history.
5. __exit__ closes the generator, then prints a summary: the register name as a header, each transaction formatted as " {amount:+d} -> {total}", and a final line with the last total. It should not suppress exceptions.

Input

with CashRegister("Daily Sales") as reg:
    reg.add(100)
    reg.add(50)
    reg.add(-30)
    reg.add(200)

Expected Output

=== Daily Sales ===
  +100 -> 100
  +50 -> 150
  -30 -> 120
  +200 -> 320
  Final: 320