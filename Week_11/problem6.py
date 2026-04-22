class CashRegister:
    def __init__(self, name):
        self.name = name

    def _accumulator(self):
        total = 0
        while True:
            amount = yield total
            total += amount

    def __enter__(self):
        self._gen = self._accumulator()
        next(self._gen)
        self._history = []
        return self

    def add(self, amount):
        total = self._gen.send(amount)
        self._history.append((amount, total))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._gen.close()

        print(f"=== {self.name} ===")
        for amount, total in self._history:
            print(f"  {amount:+d} -> {total}")
        
        final_total = self._history[-1][1] if self._history else 0
        print(f"  Final: {final_total}")

        return False

with CashRegister("Daily Sales") as reg:
    reg.add(100)
    reg.add(50)
    reg.add(-30)
    reg.add(200)