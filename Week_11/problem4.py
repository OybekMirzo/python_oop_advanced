from contextlib import contextmanager

@contextmanager
def tag(name):
    print(f"<{name}>")
    try:
        yield
    finally:
        print(f"</{name}>")

with tag("body"):
    with tag("h1"):
        print("Welcome")
    with tag("p"):
        print("Hello world")
