Variant 9: Product Assembly Line

You are building a production planning tool for a factory. Create a Component dataclass and an Assembly dataclass that handles component management, cost calculations, and scaling to different batch sizes.

1. Import dataclass and field from the dataclasses module.
2. Create a Component dataclass with fields: name (str), units (float), and price_per_unit (float).
3. Add a method total_price(self) -> float that returns units * price_per_unit.
4. `Create an Assembly dataclass with fields: title (str), batch_size (int), components (list of Component, empty by default), and a computed field total_price (float) that is not a constructor parameter. total_price must be computed in __post_init__ as the sum of every component’s price, and must stay accurate after every operation.
5. Add a method add_component(self, component: Component) that adds the component and updates total_price.
6. Add a method price_per_item(self) -> float that returns total_price / batch_size.
7. Add a method scale(self, new_batch_size: int) that adjusts every component’s units proportionally to the new batch size, updates batch_size, and recalculates total_price.
8. Add a method display(self) -> str that returns a formatted summary. Study the expected output to determine the exact format.
Always add a helper method called `_refresh(self)` that recalculates all computed fields and call it from every method that changes data

Input
a = Assembly("Drone", 8)
a.add_component(Component("Motor", 32.0, 15.0))
a.add_component(Component("Frame", 8.0, 45.0))
a.add_component(Component("Battery", 16.0, 25.0))

print(a.total_price)
print(a.price_per_item())
print(a.display())

a.scale(4)
print(a.display())

Expected Output
1240.0
155.0
Drone (8 items):
  Motor: 32.0 units ($480.0)
  Frame: 8.0 units ($360.0)
  Battery: 16.0 units ($400.0)
Per item: $155.0

Drone (4 items):
  Motor: 16.0 units ($240.0)
  Frame: 4.0 units ($180.0)
  Battery: 8.0 units ($200.0)
Per item: $155.0