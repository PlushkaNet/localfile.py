"""File with code of parser for localization documents"""

from typing import Union
import re

ParserItemSupportedType = Union[str, int, bool, float]

class ParsingError(Exception):
    """Error exception for all parsing failures"""

class ParserItem:
    def __init__(self, _format: str, simplify_behaviour: bool = False):
        """Constructs ParserItem with Python-supported {} formatting"""

        if simplify_behaviour:
            self._format = _format
            self._simplify = True
            return

        self._simplify = False
        self._format = ""
        self._expect = 0 # counter that serves number of format arguments to expect every time

        skip_next_check = False # flag to skip next symbol check
        cont = False # flag to skip next symbol
        for i, char in enumerate(_format):
            if cont:
                cont = False
                continue
            elif char == "{" and not skip_next_check:
                if len(_format)-1 > i:
                    if _format[i+1] == '}':
                        cont = True
                        self._expect += 1
                        self._format += "{}"
                        continue
                    elif _format[i+1] == '{':
                        skip_next_check = True
                        continue
                raise ParsingError(f"Parsing failed on str: {_format!r} at symbol {i+1}")
            elif skip_next_check:
                if char == "{":
                    self._format += "{{"
                elif char == "}":
                    self._format += "}}"
                else:
                    self._format += char
                skip_next_check = False
            elif char == "}":
                if len(_format)-1 > i:
                    if _format[i+1] == "}":
                        cont = True
                self._format += "}}"
            elif char == "\\" and not skip_next_check:
                skip_next_check = True
            else:
                self._format += char

    def _convert_to_str(self, item: ParserItemSupportedType):
        if isinstance(item, bool):
            return "1" if item else "0"
        return str(item)

    def __call__(self, *others: ParserItemSupportedType):
        if self._simplify:
            return self._format
        if len(others) != self._expect:
            return self._format
        return self._format.format(*(self._convert_to_str(i) for i in others))

class Localization:
    def __init__(self):
        """Constructs Localization object"""
        self._context: dict[str, ParserItem] = {} # saves all localization text by keys into dictionary
    
    def update(self, key: str, item: str):
        """Updates localization key"""
        self._context[key] = ParserItem(item.removesuffix("\n")) # removes suffix '\n', that is rudimental here

    def load(self, path: str):
        """
        Loads localization from file and parses it
        Returns self
        """
        with open(path, "r", encoding="utf-8") as file:
            key  = "" # localization key
            text = "" # localization text

            for i in file.readlines():
                if match := re.match(r"^\[(.*)\]$", i):
                    if key and text:
                        self.update(key, text)
                        text = ""

                    key = match[1]
                elif key:
                    text += i

            # final check to ensure that the whole content was read
            if key and text:
                self.update(key, text)
        return self

    def dumps(self) -> str:
        """
        Dumps self
        Returns dumped text
        """
        result = ""
        for k, v in self._context.items():
            result += f"[{k}]\n{v._format}\n"
        return result
    
    def dump(self, path: str):
        """Dumps self to file"""
        with open(path, "w", encoding="utf-8") as file:
            file.write(self.dumps())

    def __getitem__(self, key: str):
        return self._context.get(key, ParserItem(key, simplify_behaviour=True))
