class BorderedSection:
    def __init__(self, title: str):
        self.title = title

    def __enter__(self):
        self.top = f"=== {self.title} ==="
        print(self.top)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("=" * len(self.top))
        return False


with BorderedSection("Results"):
    print("Score: 95")
    print("Grade: A")