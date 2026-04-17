from dataclasses import dataclass

@dataclass
class CoffeeOrder:
    drink: str
    customer: str
    size: str = "Medium"
    price: float = 3.5

o1 = CoffeeOrder("Latte", "Paul", "Large", 4.75)
o2 = CoffeeOrder("Espresso", "Chani")
print(o1)
print(o2)