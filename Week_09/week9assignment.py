from dataclasses import dataclass, field


@dataclass
class Component:
    name: str
    units: float
    price_per_unit: float

    def total_price(self) -> float:
        return self.units * self.price_per_unit



@dataclass
class Assembly:
    title: str
    batch_size: int
    components: list[Component] = field(default_factory=list)
    total_price: float = 0.0

    def __post_init__(self):
        self.total_price = sum(c.total_price() for c in self.components)

    def add_component(self, component: Component):
        self.components.append(component)
        self.total_price += component.total_price()


    def price_per_item(self) -> float:
        return self.total_price / self.batch_size

    def scale(self, new_batch_size: int):
        factor = new_batch_size / self.batch_size

        for c in self.components:
            c.units *= factor

        self.batch_size = new_batch_size

        self.total_price = sum(c.total_price() for c in self.components)



    def display(self) -> str:
        result = f"{self.title} ({self.batch_size} items):\n"
        for c in self.components:
            result += f"  {c.name}: {c.units} units (${c.total_price():.1f})\n"
        result += f"Per item: ${self.price_per_item():.1f}"
        return result




a = Assembly("Drone", 8)
a.add_component(Component("Motor", 32.0, 15.0))
a.add_component(Component("Frame", 8.0, 45.0))
a.add_component(Component("Battery", 16.0, 25.0))

print(a.total_price)
print(a.price_per_item())
print(a.display())

a.scale(4)
print(a.display())
