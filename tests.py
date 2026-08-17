from localfile import ParserItem

assert ParserItem(r"\{\{\{")._format == "{{{{{{"
assert ParserItem(r"{{\{")._format == "{{{{"
assert ParserItem(r"\{}")._format == "{{}}"
assert ParserItem(r"C:\\file")._format == r"C:\file"
assert ParserItem(r"{}")._format == r"{}"
assert ParserItem(r"{}}}}}}}}}")._format == r"{}}}}}}}}}"
assert ParserItem(r"{}}}}}}}}}")(1) == "1}}}}"
assert ParserItem(r"\{{}\}")(1) == "{1}"

assert ParserItem("")._format == ""
assert ParserItem("abc")._format == "abc"
assert ParserItem("123")._format == "123"

assert ParserItem("{}")._format == "{}"
assert ParserItem("{}")._expect == 1
assert ParserItem("{}{}")._format == "{}{}"
assert ParserItem("{}{}")._expect == 2
assert ParserItem("{} {}")._format == "{} {}"

assert ParserItem("{{")._format == "{{"
assert ParserItem("{{")() == "{"
assert ParserItem("}}")._format == "}}"
assert ParserItem("}}")() == "}"
assert ParserItem("{{}}")._format == "{{}}"
assert ParserItem("{{}}")._expect == 0
assert ParserItem("{{}}")() == "{}"
assert ParserItem(r"\{\}")._format == "{{}}"
assert ParserItem(r"\{\}")() == "{}"
assert ParserItem(r"\{")._format == "{{"
assert ParserItem(r"\{")() == "{"
assert ParserItem(r"\}")._format == "}}"
assert ParserItem(r"\}")() == "}"

assert ParserItem("}")._format == "}}"
assert ParserItem("}")() == "}"

assert ParserItem(r"\\")._format == "\\"
assert ParserItem(r"C:\\file")._format == r"C:\file"
assert ParserItem(r"C:\file")._format == "C:file"
assert ParserItem(r"\a")._format == "a"

assert ParserItem("{}")(123) == "123"
assert ParserItem("{}")(True) == "1"
assert ParserItem("{}")(False) == "0"
assert ParserItem("{}")(3.14) == "3.14"
assert ParserItem("{} + {}")(1, 2) == "1 + 2"
assert ParserItem("{} {} {}")(1, "a", True) == "1 a 1"
assert ParserItem("{}")() == "{}"
assert ParserItem("{}")(1, 2) == "{}"

assert ParserItem(r"\{} {}")(42) == "{} 42"
assert ParserItem(r"\{{}\}")(1) == "{1}"

assert ParserItem("some_key", simplify_behaviour=True)() == "some_key"
assert ParserItem("user{id}", simplify_behaviour=True)() == "user{id}"
assert ParserItem("{literal}", simplify_behaviour=True)() == "{literal}"