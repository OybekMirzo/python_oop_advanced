Variant 9: Paint Mixer

You are building a paint mixing system. The system stores paint formulas with their pigment components and base batch sizes, can scale formulas to a desired batch count, and checks if a formula can be mixed with available pigment supplies. It must raise meaningful custom exceptions for invalid operations.

1. Create a base exception PaintError that inherits from Exception.
2. Create FormulaNotFoundError inheriting from PaintError. Its __init__ takes a formula_name parameter, stores it as an attribute, and passes the message "formula not found: {formula_name}" to the parent.
3. Create DuplicateFormulaError inheriting from PaintError. Its __init__ takes a formula_name parameter, stores it as an attribute, and passes the message "formula already exists: {formula_name}" to the parent.
4. Create InvalidBatchError inheriting from PaintError. Its __init__ takes a batches parameter, stores it as an attribute, and passes the message "invalid batches: {batches}. must be positive" to the parent.
5. Create MissingPigmentsError inheriting from PaintError. Its __init__ takes a formula_name and missing (a dictionary of pigment name to amount short) parameter, stores both as attributes, and passes the message "cannot mix {formula_name}: missing {missing}" to the parent.
6. Create a PaintMixer class with:
* __init__(self) — initializes an empty dictionary for formulas. Hint: formulas should be stored as a nested dictionary: {formula_name: {"batches": int, "pigments": {name: float}}}, e.g., {"Sunset Orange": {"batches": 2, "pigments": {"red": 4.0, "yellow": 3.0}}}.
* add_formula(self, name, batches, pigments) — adds a formula. batches is the base number of batches (int). pigments is a dictionary mapping pigment names to amounts needed (floats), e.g., {"red": 3.0, "white": 5.0}. Raises DuplicateFormulaError if the formula already exists. Raises InvalidBatchError if batches is not positive. Stores the formula data as {"batches": batches, "pigments": pigments}.
* scale_formula(self, name, desired_batches) — returns a new dictionary of pigments scaled to the desired number of batches. Uses EAFP style (try/except KeyError) to look up the formula; if not found, raises FormulaNotFoundError using from None. Raises InvalidBatchError if desired_batches is not positive. The formula is: pigment_amount * (desired_batches / base_batches), each rounded to 2 decimal places.
* check_supplies(self, name, supplies) — checks if a formula (for its base batches) can be mixed with the given supplies (a dictionary of pigment name to available amount). Uses EAFP for formula lookup. If any pigments are missing or insufficient, raises MissingPigmentsError with a dictionary of each lacking pigment and the amount short (rounded to 2 decimal places). If all pigments are sufficient, returns True.

Input

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

Expected Output

sunset orange for 6: {'red': 12.0, 'yellow': 9.0, 'white': 3.0}
ocean blue for 1: {'blue': 2.0, 'white': 1.0, 'green': 0.25}
cannot mix Sunset Orange: missing {'yellow': 2.0}
can mix ocean blue: True
formula already exists: Sunset Orange
formula not found: Forest Green
invalid batches: -4. must be positive