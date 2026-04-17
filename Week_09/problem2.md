Problem 2 (Easy+): Coffee Order

You work at a coffee shop and need to track drink orders. Create a dataclass called CoffeeOrder with default values.

1. Import dataclass from the dataclasses module.
2. Create a CoffeeOrder dataclass with four fields: drink (str), customer (str), size (str) with a default of "Medium", and price (float) with a default of 3.5.
3. Create one order with all four values: "Latte", "Paul", "Large", 4.75.
4. Create another order with only the required fields: "Espresso", "Chani".
5. Print both orders.

Input
o1 = CoffeeOrder("Latte", "Paul", "Large", 4.75)
o2 = CoffeeOrder("Espresso", "Chani")
print(o1)
print(o2)

Expected Output
CoffeeOrder(drink='Latte', customer='Paul', size='Large', price=4.75)
CoffeeOrder(drink='Espresso', customer='Chani', size='Medium', price=3.5)