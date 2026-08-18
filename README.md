# localfile

A simple, dependency-free Python library for parsing and formatting localization documents.

## Get started

Install via pip from github master branch:
```
pip install git+https://github.com/PlushkaNet/localfile.py.git
```

## Features

- Parses localization files with `[key]` sections and plain-text values
- Placeholders `{}` with Python-style `str.format()` formatting
- Literal braces via `{{` / `}}` and escaping via `\`
- Returns the original template when the number of arguments does not match
- No third-party dependencies

## Localization file format

Localization files use `[key]` sections. The text after a section header belongs to that key until the next header. Trailing newlines are removed.

```
[greeting]
Hello, world!

[greeting_personalized]
Hello, {}!

[how_to_escape]
To print {} literally, escape it: \{}
```

## Usage

```python
from localfile import Localization

loc = Localization().load("locales/en.loc")

print(loc["greeting"]())                      # Hello, world!
print(loc["greeting_personalized"]("John")) # Hello, John!
```

## API

### `ParserItem(_format, simplify_behaviour=False)`

Parses a format string with `{}` placeholders and counts the number of expected arguments (`_expect`).

Calling a `ParserItem` with arguments returns the formatted string. Supported argument types: `str`, `int`, `bool`, `float`. Booleans are converted to `"1"` / `"0"`. If the number of arguments does not match `_expect`, the original template is returned unchanged.

Escaping rules:

- `\{` and `\}` — literal `{` / `}` (requires a backslash, e.g. `\\{` for a literal backslash followed by brace)
- `{{` / `}}` — literal `{` / `}`
- `\` before any other symbol is dropped
- `{}` — placeholder

With `simplify_behaviour=True`, the item is stored as-is and calling it returns the raw string.

Raises `ParsingError` on malformed format strings.

```python
from localfile import ParserItem

item = ParserItem("Hello, {}!")
item("World")            # Hello, World!
item()                   # Hello, {}! (wrong arg count -> template returned)

ParserItem("{}")(True)   # "1"
ParserItem(r"\{").format  # literal "{" (needs escaping to display here)
ParserItem(r"\{} {}")(42)  # "{} 42"
```

### `Localization`

- `load(path)` — loads and parses a localization file; returns `self`
- `update(key, item)` — sets a localization key from a string
- `dumps()` — returns the whole context as a text in the `[key]` file format
- `dump(path)` — writes the context to a file
- `loc[key]` — returns a `ParserItem` for the key; missing keys return the key itself as a literal (via `simplify_behaviour`)

### `ParsingError`

Exception raised on any parsing failure.

## Tests

Run the assert-based test suite (no dependencies required):

```bash
python tests.py
```

## License

[MIT](./LICENSE)
