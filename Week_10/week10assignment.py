class PaintError(Exception):
    pass

class FormulaNotFoundError(PaintError):
    def __init__(self, formula_name):
        self.formula_name = formula_name
        super().__init__(f"formula not found: {formula_name}")

class DuplicateFormulaError(PaintError):
    def __init__(self, formula_name):
        self.formula_name = formula_name
        super().__init__(f"formula already exists: {formula_name}")


class InvalidBatchError(PaintError):
    def __init__(self, batches):
        self.batches = batches
        super().__init__(f"invalid batches: {batches}. must be positive")

class MissingPigmentsError(PaintError):
    def __init__(self, formula_name, missing):
        self.formula_name = formula_name
        self.missing = missing
        super().__init__(f"cannot mix {formula_name}: missing {missing}")


class PaintMixer:
    def __init__(self):
        self.formulas = {}


    def add_formula(self, name, batches, pigments):
        if name in self.formulas:
            raise DuplicateFormulaError(name)
        if batches <= 0:
            raise InvalidBatchError(batches)
        self.formulas[name] = {"batches": batches, "pigments": pigments}

    def scale_formula(self, name, desired_batches):
        try:
            formula = self.formulas[name]
        except KeyError:
            raise FormulaNotFoundError(name) from None

        if desired_batches <= 0:
            raise InvalidBatchError(desired_batches)

        base_batches = formula["batches"]
        return {
            pigment: round(amount * (desired_batches / base_batches), 2)
            for pigment, amount in formula["pigments"].items()
        }
    def check_supplies(self, name, supplies):
        try:
            formula = self.formulas[name]
        except KeyError:
            raise FormulaNotFoundError(name) from None


        missing = {}
        for pigment, needed in formula["pigments"].items():
            available = supplies.get(pigment, 0)
            if available < needed:
                missing[pigment] = round(needed - available, 2)

        if missing:
            raise MissingPigmentsError(name, missing)
        return True


mixer = PaintMixer()

mixer.add_formula("Sunset Orange", 2, {"red": 4.0, "yellow": 3.0, "white": 1.0})
mixer.add_formula("Ocean Blue", 3, {"blue": 6.0, "white": 3.0, "green": 0.75})

scaled = mixer.scale_formula("Sunset Orange", 6)
print(f"sunset orange for 6: {scaled}")

scaled = mixer.scale_formula("Ocean Blue", 1)
print(f"ocean blue for 1: {scaled}")

supplies = {"red": 4.0, "yellow": 1.0, "white": 1.0}
try:
    mixer.check_supplies("Sunset Orange", supplies)
except PaintError as e:
    print(e)

supplies2 = {"blue": 10.0, "white": 5.0, "green": 2.0}
result = mixer.check_supplies("Ocean Blue", supplies2)
print(f"can mix ocean blue: {result}")

tests = [
    lambda: mixer.add_formula("Sunset Orange", 2, {"red": 1.0}),
    lambda: mixer.scale_formula("Forest Green", 3),
    lambda: mixer.scale_formula("Ocean Blue", -4),
]

for test in tests:
    try:
        test()
    except PaintError as e:
        print(e)