#!/usr/bin/env python3

import sys
import pathlib
import argparse

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from source_translator import SourceCode, c_like
from source_translator.langs import cpp, ts, php
from source_translator.naming import snake_to_lower_camel

translators = {
    "cpp": cpp.CppTranslator(),
    "ts": ts.TypeScriptTranslator(),
    "js": ts.TypeScriptTranslator(False),
    "php": php.PhpTranslator(),
}
translators["c++"] = translators["cpp"]


styles = {
    "allman": c_like.AllmanStyle(),
    "k&r": c_like.KandRStyle(),
    "whitesmiths": c_like.WhitesmithsStyle(),
    "gnu": c_like.GnuStyle()
}


parser = argparse.ArgumentParser()
parser.add_argument("file", type=pathlib.Path)
parser.add_argument("--language", "-x", choices=translators.keys())
parser.add_argument("--style", "-s", choices=styles.keys())
parser.add_argument("--indent-width", "-w", type=int, default=4)
parser.add_argument("--camel", action="store_true")
args = parser.parse_args()

with open(args.file) as f:
    source = SourceCode(f.read())

translator = translators[args.language]

if args.style:
    translator.indent_style = styles[args.style]

if args.indent_width:
    translator.indent_style.spaces = args.indent_width


translator.naming_style = snake_to_lower_camel if args.camel else str

output = translator.convert(source)
print(output)
