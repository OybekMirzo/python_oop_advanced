Week 10 Lecture: Exception Handling

This week covers exception handling in the context of object-oriented programming. You will learn how to create custom exception classes, build exception hierarchies for your projects, and apply Python’s preferred error-handling philosophy.

Review: Exceptions and try/except
When Python encounters a problem during execution, it raises an exception. If no code catches the exception, the program crashes.

print(10 / 0)

ZeroDivisionError: division by zero

To prevent crashing, wrap risky code in a try/except block:

try:
    result = 10 / 0
except ZeroDivisionError:
    print("you cannot divide by zero!")

The else clause runs only when no exception occurred, and finally runs regardless of whether an exception was raised:

try:
    result = 10 / 2
except ZeroDivisionError:
    print("cannot divide by zero!")
else:
    print(f"result is {result}")
finally:
    print("this always runs")

The Exception Hierarchy
All exceptions in Python are classes arranged in an inheritance hierarchy. At the top is BaseException. The class Exception inherits from it, and all common error types inherit from Exception:

BaseException
├── KeyboardInterrupt
├── SystemExit
└── Exception
    ├── ValueError
    ├── TypeError
    ├── KeyError
    ├── FileNotFoundError
    ├── ZeroDivisionError
    ├── AttributeError
    └── ... (many more)

This hierarchy matters because except Exception catches everything that inherits from Exception — including ValueError, TypeError, KeyError, and so on. That is usually too broad. Always be specific: if you expect a ValueError, catch ValueError.

Using raise in Classes
The raise keyword lets you manually throw an exception when something goes wrong. In OOP, raise is commonly used inside methods to reject invalid data:

class BankAccount:
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount

However, using generic exceptions like ValueError for every kind of problem makes it difficult for the caller to distinguish between different failure reasons without inspecting the error message string. Custom exceptions solve this problem.

Creating Custom Exceptions
Creating a custom exception is straightforward — define a class that inherits from Exception:

class InsufficientFundsError(Exception):
    pass

The pass keyword means no additional behavior is needed. Simply inheriting from Exception makes it a fully functional exception class.

Why inherit from Exception and not BaseException? Because BaseException includes system-level events like KeyboardInterrupt and SystemExit. The Exception class is the proper parent for application-level errors — things that went wrong in your code.

Here is a more complete example using two custom exceptions:

class InsufficientFundsError(Exception):
    pass

class NegativeAmountError(Exception):
    pass

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise NegativeAmountError('amount must be positive')
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise NegativeAmountError('amount must be positive')
        if amount > self.balance:
            raise InsufficientFundError('not enough funds')
        self.balance -= amount

Now the caller can handle each error type separately:

acc = BankAccount("Sevara", 500)

try:
    acc.withdraw(1000)
except InsufficientFundsError as e:
    print(f"not enough money: {e}")
except NegativeAmountError as e:
    print(f"invalid amount: {e}")

Each error has its own type, so you can catch them independently and respond differently.

Exceptions with Extra Data
Sometimes an exception needs to carry more information than just a message. For instance, an InsufficientFundsError could store the requested amount and the current balance.

To do this, override __init__ in your exception class:

class InsufficientFundsError(Exception):
    def __init__(self, amount, balance):
        self.amount = amount
        self.balance = balance
        self.deficit = amount - balance
        super().__init__(
            f"cannot withdraw {amount}: balance is {balance}, short by {self.deficit}"
        )

The call to super().__init__() passes the formatted message string to Exception.__init__(), which sets it as the default string representation of the error.

When raising this exception, you pass numeric values instead of a message string:

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(amount, self.balance)
        self.balance -= amount

When catching it, you can access both the message and the individual attributes:

acc = BankAccount("Jasur", 500)

try:
    acc.withdraw(800)
except InsufficientFundsError as e:
    print(e)             # cannot withdraw 800: balance is 500, short by 300
    print(e.amount)      # 800
    print(e.balance)     # 500
    print(e.deficit)     # 300

The exception is no longer just a message — it is an object with attributes. You can use those attributes to make smart decisions, such as withdrawing the remaining balance or suggesting a smaller amount.

Building an Exception Hierarchy
For larger projects, it is good practice to create your own exception hierarchy. Define a base exception for your project, then have specific exceptions inherit from it:

class BankError(Exception):
    """Base exception for all banking errors"""
    pass

class InsufficientFundsError(BankError):
    pass

class NegativeAmountError(BankError):
    pass

class AccountClosedError(BankError):
    pass

This gives users of your code flexibility in how precisely they handle errors:

# catch only insufficient funds
try:
    acc.withdraw(1000)
except InsufficientFundsError:
    print("not enough money")

# catch any banking error
try:
    acc.withdraw(1000)
except BankError:
    print("something went wrong with the bank")

except BankError will catch InsufficientFundsError, NegativeAmountError, and AccountClosedError because they all inherit from BankError. This follows the same principle as except Exception catching everything, but scoped to your project.

Naming Conventions for Exceptions
Python has a strong convention for naming exception classes:

Always end with Error: InsufficientFundsError, not InsufficientFunds. NegativeAmountError, not BadAmount. AccountClosedError, not ClosedAccountProblem.
Use descriptive names: The name alone should tell you what went wrong, without reading the message. InvalidEmailError is clear; Error1 is not.
Every built-in exception follows this pattern (ValueError, TypeError, KeyError, FileNotFoundError), and your custom exceptions should look like they belong in the same family.

EAFP vs LBYL
Python has a preferred philosophy for handling potential errors called EAFP — “Easier to Ask Forgiveness than Permission.” The opposite style is LBYL — “Look Before You Leap.”

Dictionary Access Example
LBYL style — check first, then act:

student = {"name": "Alisher", "gpa": 3.8}

if "name" in student:
    print(student["name"])
else:
    print("key not found")

EAFP style — just do it, handle the error if it happens:

student = {"name": "Alisher", "gpa": 3.8}

try:
    print(student["name"])
except KeyError:
    print("key not found")

Both work, but Python prefers EAFP for two reasons:

Performance: LBYL performs two lookups (check + access), while EAFP performs one. Since the error path rarely executes, EAFP is typically faster.
No race conditions: LBYL has a gap between the check and the action. In that gap, the state could change. This is called a TOCTOU bug (Time Of Check to Time Of Use).
Consider file access:

# LBYL - has a gap!
import os
if os.path.exists("data.txt"):
    # what if someone deletes the file RIGHT HERE?
    f = open("data.txt")

Between checking and opening, another process could delete the file. With EAFP, there is no gap:

# EAFP - no gap
try:
    f = open("data.txt")
except FileNotFoundError:
    print("file not found")

EAFP and Duck Typing
EAFP works naturally with duck typing. When you have objects that may or may not support a method, just try calling it:

LBYL approach:

def get_area(shape):
    if hasattr(shape, 'area'):
        return shape.area()
    else:
        return "no area method"

EAFP approach:

def get_area(shape):
    try:
        return shape.area()
    except AttributeError:
        return "no area method"

Converting User Input
LBYL — check if the value is a valid number first:

value = input("enter a number: ")

if value.isnumeric():
    number = float(value)
else:
    print("not a valid number")

This has problems: "3.5".isnumeric() returns False, and so does "-5".isnumeric(). The check is incomplete.

EAFP — just try to convert:

value = input("enter a number: ")

try:
    number = float(value)
except ValueError:
    print("not a valid number")

This is cleaner, simpler, and handles all edge cases because float() itself knows exactly what constitutes a valid number.

Comprehensive Example: Student Registry
This section combines all the concepts covered this week into a complete example — a StudentRegistry class that manages students with a full custom exception hierarchy.

Defining the Exception Hierarchy
First, define a base exception for the registry:

class RegistryError(Exception):
    """Base exception for registry errors"""
    pass

Then create three specific exceptions, each storing the problematic value as an attribute:

StudentNotFoundError — raised when looking up a student that does not exist:

class StudentNotFoundError(RegistryError):
    def __init__(self, student_id):
        self.student_id = student_id
        super().__init__(f"no student found with id: {student_id}")

DuplicateStudentError — raised when adding a student with an ID that already exists:

class DuplicateStudentError(RegistryError):
    def __init__(self, student_id):
        self.student_id = student_id
        super().__init__(f"student with id {student_id} already exists")

InvalidGradeError — raised when a grade is outside the 0–100 range:

class InvalidGradeError(RegistryError):
    def __init__(self, grade):
        self.grade = grade
        super().__init__(f"invalid grade: {grade}. must be between 0 and 100")

Notice the pattern: every exception stores the bad value as an attribute and passes a descriptive message to super().__init__(). The caller can either print the message or access the attribute directly. And because they all inherit from RegistryError, you can catch all registry problems with except RegistryError, or catch each one individually.

The Registry Class
class StudentRegistry:
    def __init__(self):
        self._students = {}

    def add_student(self, student_id, name):
        if student_id in self._students:
            raise DuplicateStudentError(student_id)
        self._students[student_id] = {"name": name, "grades": []}

    def add_grade(self, student_id, grade):
        # EAFP style — just try to access the student
        try:
            student = self._students[student_id]
        except KeyError:
            raise StudentNotFoundError(student_id)

        if not 0 <= grade <= 100:
            raise InvalidGradeError(grade)

        student["grades"].append(grade)

    def get_average(self, student_id):
        try:
            student = self._students[student_id]
        except KeyError:
            raise StudentNotFoundError(student_id)

        if not student["grades"]:
            raise RegistryError(f"student {student_id} has no grades yet")

        return sum(student["grades"]) / len(student["grades"])

The add_grade method demonstrates two important techniques:

EAFP to check if the student exists — it tries to access the student directly rather than checking first.
Exception translation — it catches KeyError (an implementation detail of using a dictionary) and raises StudentNotFoundError (a meaningful error for the caller). The caller should not need to know that the registry uses a dictionary internally.
Exception Translation and Chaining
When you catch a low-level exception and raise a higher-level one, this is called exception translation. However, the way you raise the new exception affects the traceback.

raise ... from ...
When you write raise StudentNotFoundError(student_id) inside an except KeyError block, Python shows both exceptions but the connection is unclear — it says “during handling of the above exception, another exception occurred.”

To make the connection explicit, use raise ... from ...:

def add_grade(self, student_id, grade):
    try:
        student = self._students[student_id]
    except KeyError as e:
        raise StudentNotFoundError(student_id) from e

Now Python says “the above exception was the direct cause of the following exception” — much clearer.

raise ... from None
You can also suppress the original exception entirely with from None:

except KeyError:
    raise StudentNotFoundError(student_id) from None

This hides the original KeyError from the traceback. Use this when the original error is purely an implementation detail that would only confuse the caller.

Summary of chaining behavior:

Syntax	Behavior
raise X inside except	Shows both errors; connection is unclear
raise X from e	Shows both errors; clearly states one caused the other
raise X from None	Shows only your error; hides the original
Re-raising Exceptions
Sometimes you want to perform an action (such as logging) when an exception occurs but still let the same exception propagate upward. Use a bare raise for this:

def add_grade(self, student_id, grade):
    try:
        student = self._students[student_id]
    except KeyError:
        print(f"WARNING: someone tried to access student {student_id}")
        raise

The bare raise re-raises the same KeyError that was caught. The traceback is fully preserved — it looks exactly as if you never caught it. This is useful for logging errors before they propagate:

class StudentRegistry:
    def add_grade(self, student_id, grade):
        try:
            student = self._students[student_id]
        except KeyError:
            log_error(f"student {student_id} not found")
            raise

The caller still receives the KeyError and can handle it however they want. You simply added logging without changing the error behavior.

Common Anti-Patterns
These are common mistakes to avoid when working with exceptions.

Anti-Pattern 1: Bare except
try:
    acc.withdraw(500)
except:
    print("something went wrong")

A bare except catches everything, including KeyboardInterrupt and SystemExit. This means pressing Ctrl+C will not stop your program — it will print “something went wrong” and continue. Always specify which exception you want to catch.

Anti-Pattern 2: Catching and Doing Nothing
try:
    acc.withdraw(500)
except InsufficientFundsError:
    pass

This silently swallows the error. The withdrawal failed, but nothing in the program reflects that. This leads to bugs that are extremely difficult to track down. If you catch an exception, always do something useful: log it, display a message, retry the operation, or re-raise it.

Anti-Pattern 3: Catching Exception for Everything
try:
    result = calculate_grade(student)
except Exception:
    print("error")

This is too broad. If a TypeError occurs because of a bug in your code, you will never see it — the program just prints “error” and continues with the bug hidden. Always catch specific exceptions. If you expect a ValueError, catch ValueError.