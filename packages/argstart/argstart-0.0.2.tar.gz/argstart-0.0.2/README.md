# argstart

Lets you define a "main" function to be run automatically. If that function has arguments, they'll be turned into command-line arguments.

So you can do:

```python
from argstart import start

@start
def main(in_path: str, out_path: str, timeout: int = 500):
    ...
```

Instead of:

```python
from argparse import ArgumentParser

def main(in_path: str, out_path: str, timeout: int = 500):
    ...

...

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("in_path", type=str)
    parser.add_argument("out_path", type=str)
    parser.add_argument("-t", "--timeout", type=int, default=500)
    args = parser.parse_args()

    main(args.in_path, args.out_path, args.timeout)
```

## More details

**Mostly:** just write the function as you normally would, and it should work as you expect. 

Use `python your_file.py --help` for full generated usage, like with argparse.

If specified, type annotations will be used to determine the command-line argument type.

Parses common docstring formats using [docstring-parser](https://pypi.org/project/docstring-parser/) to add command and argument descriptions.

So that all your functions get defined first, the main function is called at the end of your script - not immediately when it's defined/decorated. This is the same as if you had `if __name__ == "__main__"` at the bottom.

Command-line `--flags` also get a short acronym you can use instead, like `-f`.

It's command-line convention that flags are optional and positional arguments are required, so this is how arguments are translated by default:

```python
def main(one, two, foo=1, bar=2)
# command-line: example.py [-f FOO] [-b BAR] one two
```

But you could force required arguments to become *required flags* by making them keyword-only:

```python
def main(one, *, two, foo=1, bar=2)
# command-line: example.py -t TWO [-f FOO] [-b BAR] one
```

Or force optional arguments to become *optional positional arguments* by making them positional-only:

```python
def main(one, two, foo=1, /, bar=2)
# command-line: example.py [-b BAR] one two [foo]
```

Supports `*args` and `**kwargs`:

```python
def main(foo, *bar)
# command-line: example.py foo [bar ...]

def main(foo, **bar)
# command-line: example.py [-b [BAR ...]] foo
```

Finally, booleans will by default create a `--toggle-flag` which don't require any value after:
```python
def main(foo=False)
# command-line: example.py [-f]
# (meaning foo defaults to False when -f flag is not given)
```
