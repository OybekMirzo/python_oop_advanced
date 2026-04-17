Problem 3 (Medium): Cargo Crate

You are managing cargo shipments across planets. Create a CargoCrate dataclass that tracks its contents and enforces a weight limit.

1. A CargoCrate has fields: crate_id (str), destination (str), max_weight (float), and items which starts as an empty list of (name, weight) tuples.
2. total_weight(self) -> float — returns the combined weight of all items in the crate.
3. add_item(self, name: str, weight: float) -> bool — adds the item only if doing so would not exceed the crate’s weight limit. Returns whether the item was successfully added.
4. manifest(self) — prints a formatted summary of the crate. Study the expected output to determine the exact format.

Input
c = CargoCrate("CR-401", "Arrakis", 50.0)
print(c.add_item("Stillsuit", 8.5))
print(c.add_item("Spice Melange", 30.0))
print(c.add_item("Shield Generator", 15.0))
print(c.total_weight())
c.manifest()

Expected Output
True
True
False
38.5
Crate CR-401 -> Arrakis
  - Stillsuit: 8.5kg
  - Spice Melange: 30.0kg
Total: 38.5/50.0kg