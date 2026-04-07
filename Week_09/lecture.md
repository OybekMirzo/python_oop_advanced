Week 9 Lecture: Dataclasses

The Problem with Boilerplate Code
Over the past weeks, we have been writing classes like this:

class Student:
    def __init__(self, name, student_id, gpa):
        self.name = name
        self.student_id = student_id
        self.gpa = gpa

Notice how each attribute name is written three times: once in the parameter list, once as self.name, and once as the assigned value. For three attributes, that is nine repetitions just in __init__. A class with ten attributes would require thirty repetitions — and that does not even include __repr__ or __eq__.

A proper Student class with __init__, __repr__, and __eq__ looks like this:

class Student:
    def __init__(self, name, student_id, gpa):
        self.name = name
        self.student_id = student_id
        self.gpa = gpa

    def __repr__(self):
        return f"Student(name={self.name!r}, student_id={self.student_id!r}, gpa={self.gpa!r})"

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return (self.name == other.name and 
                self.student_id == other.student_id and 
                self.gpa == other.gpa)

Nothing here is surprising — it is all predictable, mechanical code. What if the same class could be written in just five lines?

The dataclasses Module
The dataclasses module lets Python automatically generate boilerplate methods for classes that primarily hold data. To use it, import the dataclass decorator from the dataclasses module, apply it to your class, and define your fields using type annotations:

from dataclasses import dataclass

@dataclass
class Student:
    name: str
    student_id: str
    gpa: float

Although these look like class variables, the @dataclass decorator turns them into instance variables by automatically generating an __init__ method that saves them via self. Each variable must include a type annotation.

This single decorator automatically provides __init__, __repr__, and __eq__:

s1 = Student("Alisher", "2024001", 3.8)
s2 = Student("Alisher", "2024001", 3.8)

print(s1)          # Student(name='Alisher', student_id='2024001', gpa=3.8)
print(s1 == s2)    # True

How @dataclass Works Under the Hood
Recall that a decorator is a function that takes something and returns a modified version of it. The @dataclass decorator takes your class and returns a modified version with auto-generated methods. Since everything in Python is an object — including classes — they can be passed as parameters.

When Python encounters the @dataclass decorator above a class:

It examines the class body for type-annotated variables.
It generates an __init__ method using those variable names as parameters.
It generates __repr__ and __eq__ methods.
It attaches all generated methods to the class.
Here is a simplified implementation that illustrates the process:

def my_dataclass(cls):
    """A simplified version of Python's @dataclass"""
    
    # STEP 1: Look at the class body for labeled variables (annotations)
    # __annotations__ is a hidden dictionary Python creates when you type label variables.
    # For example: {'name': <class 'str'>, 'age': <class 'int'>}
    fields = cls.__annotations__ 

    # STEP 2: Generate an __init__ method
    def new_init(self, *args, **kwargs):
        # This matches the passed arguments to the expected fields
        for field_name, value in zip(fields.keys(), args):
            setattr(self, field_name, value)
            
        for key, value in kwargs.items():
            setattr(self, key, value)

    # STEP 3: Generate a __repr__ method (for printing)
    def new_repr(self):
        # Creates a string like: Student(name='Alice', age=20)
        field_strings = []
        for field_name in fields.keys():
            value = getattr(self, field_name)
            field_strings.append(f"{field_name}={repr(value)}")
            
        joined_fields = ", ".join(field_strings)
        return f"{cls.__name__}({joined_fields})"

    # STEP 4: Generate an __eq__ method (for checking ==)
    def new_eq(self, other):
        if not isinstance(other, cls):
            return False
        # Check if all fields are identical
        for field_name in fields.keys():
            if getattr(self, field_name) != getattr(other, field_name):
                return False
        return True

    # STEP 5: Add them to your class
    cls.__init__ = new_init
    cls.__repr__ = new_repr
    cls.__eq__ = new_eq

    # Return the newly modified class!
    return cls

Default Values
Fields can have default values, specified after the type annotation:

from dataclasses import dataclass

@dataclass
class Student:
    name: str
    student_id: str
    gpa: float = 0.0
    year: int = 1

s = Student("Sevara", "2024015")
print(s)  # Student(name='Sevara', student_id='2024015', gpa=0.0, year=1)

Important rule: Fields with default values must come after fields without defaults. This is the same rule Python applies to function parameters. If a parameter has a default value, all parameters after it must also have defaults. Otherwise, Python cannot determine which argument maps to which parameter.

@dataclass
class Student:
    name: str = "Unknown"   # has default
    student_id: str          # no default — ERROR!

This raises a TypeError: non-default argument 'student_id' follows default argument.

Mutable Default Values and field()
Using a mutable object like a list as a default value is not allowed in dataclasses:

@dataclass
class Student:
    name: str
    grades: list = []  # ValueError!

Python raises ValueError: mutable default <class 'list'> for field grades is not allowed: use default_factory. The decorator actively prevents the shared-mutable-default bug.

To safely provide a mutable default, import the field function and use default_factory:

from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    student_id: str
    grades: list = field(default_factory=list)

This tells Python: every time a new Student is created, call list() to produce a fresh empty list. Each object gets its own list — no sharing.

Note that list is passed without parentheses — it is the function itself being passed, not its result. The dataclass will call it later when needed. Writing default_factory=lambda: [] achieves the same result.

Why does list work both as a type and as a callable? In Python, list is both a type (used in isinstance checks) and a callable (used to create new lists). In fact, all types in Python are callable — when you write Student("Alisher", "2024001"), you are calling the Student class as a function.

s1 = Student("Jasur", "2024020")
s2 = Student("Nodira", "2024021")

s1.grades.append(90)

print(s1.grades)  # [90]
print(s2.grades)  # [] — safe! not shared

Use field(default_factory=...) any time the default value is a list, dict, set, or any other mutable object.

Adding Methods to a Dataclass
A dataclass is still a regular class. The @dataclass decorator only auto-generates methods like __init__, __repr__, and __eq__ — everything else remains completely normal. You can add instance methods, static methods, or class methods. You can even make a dataclass abstract by inheriting from ABC.

from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    student_id: str
    gpa: float = 0.0
    grades: list = field(default_factory=list)

    def add_grade(self, grade):
        self.grades.append(grade)
        self.gpa = sum(self.grades) / len(self.grades)

    def is_passing(self):
	    return self.gpa >= 60

s = Student("Alisher", "2024001")
s.add_grade(95)
s.add_grade(88)
s.add_grade(92)

print(s)
# Student(name='Alisher', student_id='2024001', gpa=91.666..., grades=[95, 88, 92])

print(s.is_passing())  # True

@dataclass handles the boring parts so you can focus on the interesting ones.

Frozen (Immutable) Dataclasses
Sometimes an object should not be changed after creation. To make a dataclass immutable, pass frozen=True:

from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(3.0, 4.0)
print(p)        # Point(x=3.0, y=4.0)

p.x = 10.0     # FrozenInstanceError!

Setting frozen=True makes the object immutable — no attribute can be changed after creation. Any attempt raises a FrozenInstanceError.

Why is this useful?

Safety: Some objects should never change, such as geographic coordinates.
Hashability: Frozen dataclasses can be used as dictionary keys or in sets.
p1 = Point(3.0, 4.0)
p2 = Point(1.0, 2.0)

locations = {p1: "Tashkent", p2: "Samarkand"}
print(locations[p1])  # "Tashkent"

Regular classes and regular dataclasses cannot be used as dictionary keys because mutable objects are not hashable by default.

Hashability means Python can compute a fixed number (a hash) from the object. This hash is used for fast lookups in dict and set. If an object can change, its hash could change too, breaking lookups. Therefore, Python only allows immutable objects to be hashable. Setting frozen=True guarantees the object will not change, making it hashable.

__post_init__: Running Code After Initialization
Sometimes the auto-generated __init__ is not enough — you may need to compute a value from other fields. Consider a Rectangle with width and height provided by the user, and an area that should be calculated automatically.

The problem: every type-annotated variable becomes a parameter in __init__. Writing area: float would make Python expect area as an argument. To exclude it from the constructor, use field(init=False):

from dataclasses import dataclass, field

@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)  # not a constructor parameter

Now area will not appear in __init__, so you create a rectangle with just Rectangle(5.0, 3.0). But area still needs a value — this is where __post_init__ comes in. It is a special method that runs immediately after the auto-generated __init__ finishes:

    def __post_init__(self):
        self.area = self.width * self.height

The sequence of events when you write Rectangle(5.0, 3.0):

Python calls the auto-generated __init__, which sets width and height.
At the end of __init__, Python automatically calls __post_init__.
Inside __post_init__, area is calculated.
r = Rectangle(5.0, 3.0)
print(r)  # Rectangle(width=5.0, height=3.0, area=15.0)
print(r.area)  # 15.0

Note that area appears in the __repr__ output. Normally, __repr__ shows how to recreate the object, but trying Rectangle(5.0, 3.0, 15.0) would raise an error since area is not a constructor parameter. If you want to be strictly accurate, you can hide it with repr=False:

area: float = field(init=False, repr=False)

Why declare area as a field instead of just assigning it in __post_init__? You could simply write self.area = self.width * self.height in __post_init__ without declaring it as a field. However, if area is not declared as a field, the dataclass does not know about it — it will not appear in __repr__ and will not be used in __eq__ comparisons. Using field(init=False) makes area a proper dataclass field, included in both __repr__ and __eq__.

Ordering with order=True
The @dataclass decorator auto-generates __eq__, but not comparison methods (__lt__, __gt__, __le__, __ge__). To get those as well, use order=True:

from dataclasses import dataclass

@dataclass(order=True)
class Student:
    gpa: float
    name: str  
    student_id: str 

Ordering is the ability to compare two objects. Think of five students standing in no particular arrangement — there is no order. Now ask them to line up from lowest GPA to highest, and you have an order that allows comparison.

How the comparison methods work: The generated methods put all attributes into a tuple in the order they are defined, and compare the tuples. Recall how tuple comparison works in Python:

(3.8, "Alisher") > (3.5, "Sevara") is True because 3.8 > 3.5.
(3.8, "Alisher") > (3.8, "Zafar") is False because the first elements are equal, so Python compares the second: "A" < "Z".
The generated __lt__ method looks like this:

def __lt__(self, other):
    if not isinstance(other, Student):
        return NotImplemented
    # It compares them as if they were tuples of their fields
    return (self.gpa, self.name, self.student_id) < (other.gpa, other.name, other.student_id)

Field order matters. The first field becomes the primary sort key. If the first fields are equal, comparison moves to the second field, and so on.

from dataclasses import dataclass

@dataclass(order=True)
class Student:
    gpa: float        # Primary sort key
    name: str         # Secondary (tie-breaker)
    student_id: str   # Final tie-breaker

s1 = Student(3.8, "Alisher", "2024001")
s2 = Student(3.5, "Sevara", "2024015")

print(s1 > s2)   # True (3.8 > 3.5)

students = [s1, s2, Student(3.8, "Zafar", "2024020")]
print(sorted(students))
# Sorted by gpa first, then name. 
# "Alisher" (3.8) will come before "Zafar" (3.8).

When to Use Dataclasses
Use @dataclass when your class is primarily about storing data and you are comfortable with auto-generated magic methods.
Use a regular class when your class is primarily about behavior or you need fine-grained control over its methods.
Type Hints for Collections
Beyond simple types, Python supports type hints for collections and nested structures:

names: list[str] = ["Alisher", "Sevara", "Jasur"]
scores: dict[str, int] = {"Alisher": 95, "Sevara": 88}
coordinates: tuple[float, float] = (41.2995, 69.2401)
unique_ids: set[int] = {101, 102, 103}

For more complex nested data:

all_grades: list[list[int]] = [[90, 85, 88], [76, 92], [100, 95, 89, 91]]

student_grades: dict[str, list[int]] = {
    "Alisher": [90, 85, 88],
    "Sevara": [76, 92, 100],
}

leaderboard: list[tuple[str, int]] = [("Alisher", 95), ("Sevara", 88), ("Jasur", 72)]

course_results: dict[str, dict[str, int]] = {
    "OOP": {"Alisher": 90, "Sevara": 85},
    "Calculus": {"Alisher": 78, "Jasur": 92},
}

Optional and Union Types
When a value might be None, use the union syntax:

def get_phone(student_id: str) -> str | None:
    ...
Cop
When a value can be one of several types:

def find_student(identifier: str | int):
    ...

Combining Dataclasses with Type Hints
Here is a complete example bringing everything together:

from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    student_id: str
    gpa: float = 0.0
    grades: list[int] = field(default_factory=list)
    email: str | None = None
    courses: dict[str, str] = field(default_factory=dict)

s = Student(
    name="Nodira",
    student_id="2024030",
    gpa=3.7,
    grades=[90, 85, 92],
    email="nodira@alkhu.uz",
    courses={"CS201": "OOP", "MATH101": "Calculus"}
)

Forward References
Consider a class that references itself:

@dataclass
class Employee:
    name: str
    manager: Employee  # ERROR!

When Python encounters manager: Employee, the Employee class is not yet fully defined — it raises a NameError. The fix is to use a string instead:

@dataclass
class Employee:
    name: str
    manager: 'Employee'  # OK — forward reference

By using a string, you tell Python: “do not resolve this name now; check it later.” This is called a forward reference.

Forward references are needed in two situations:

Self-reference: A class refers to itself (e.g., an employee whose manager is also an employee).
Cross-reference: A class refers to another class defined later in the file.
@dataclass
class Gradebook:
    students: list['Student']  # Student is defined below

@dataclass
class Student:
    name: str

Type-Hinting Callable Objects
Functions passed as arguments can also be type-hinted using Callable from the typing module:

from typing import Callable

def apply_operation(x: int, y: int, operation: Callable[[int, int], int]) -> int:
    return operation(x, y)

def add(a: int, b: int) -> int:
    return a + b

result = apply_operation(5, 3, add)  # 8

Callable[[int, int], int] means a function that takes two int parameters and returns an int. The first part (inside the inner brackets) specifies the parameter types, and the second part specifies the return type.