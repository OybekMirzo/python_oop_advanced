Problem 4 (Medium+): Tag Wrapper with `@contextmanager`

You are building a simple HTML renderer for the console. Write a generator-based context manager using the @contextmanager decorator that prints an opening HTML tag when the block starts and a closing tag when it ends — even if an error occurs inside.

1. Import contextmanager from contextlib.
2. Create a function tag that accepts one parameter: name (the tag name).
3. Print "<name>" before yield, and "</name>" after.
4. Use try/finally so the closing tag always prints.

Input
with tag("body"):
    with tag("h1"):
        print("Welcome")
    with tag("p"):
        print("Hello world")

Expected Output
<body>
<h1>
Welcome
</h1>
<p>
Hello world
</p>
</body>