"""Main module."""

import pandas as pd
import logging
import itertools
import re
from pyparsing import *

from ruleminer.const import DUNDER_DF

AND = one_of(["AND", "and", "&"])
OR = one_of(["OR", "or", "|"])
NOT = one_of(["NOT", "~"])
SEP = Literal(",")

QUOTE = Literal("'") | Literal('"')
ARITH_OP = one_of("+ - * /")
LOGIC_OP = one_of("& |")
COMPA_OP = one_of(">= > <= < != == in")
PREFIX_OP = one_of("min max abs quantile MIN MAX ABS QUANTILE")
NUMBER = Combine(Word(nums) + "." + Word(nums)) | Word(nums)
STRING = srange(r"[a-zA-Z0-9_.,:;<>*=+-/\\?|@#$%^&()']") + " "
COLUMN = Combine("{" + QUOTE + Word(STRING) + QUOTE + "}")
QUOTED_STRING = Combine(QUOTE + Word(STRING) + QUOTE)

PARL = Literal("(").suppress()
PARR = Literal(")").suppress()

# STRING_2 = srange(r"[a-zA-Z0-9_.,:;*+-/\\?|@#$%^&']") + " "
# COLUMN_VARIABLE = (PARL+Literal("?P<")+Word(STRING_2)+Literal(">")+COLUMN+PARR) | (PARL+Literal("?P=")+Word(STRING_2)+PARR)

ARITH_COLUMNS = Group((COLUMN | NUMBER) + (ARITH_OP + (COLUMN | NUMBER))[1, ...])
COLUMNS = (PARL + ARITH_COLUMNS + PARR) | ARITH_COLUMNS | COLUMN | NUMBER
PREFIX_COLUMN = PREFIX_OP + Group(PARL + COLUMNS + (SEP + COLUMNS)[0, ...] + PARR)
QUOTED_STRING_LIST = Group(
    Literal("[") + QUOTED_STRING + (SEP + QUOTED_STRING)[0, ...] + Literal("]")
)

# TERM = PREFIX_COLUMN | COLUMNS | QUOTED_STRING | QUOTED_STRING_LIST | COLUMN_VARIABLE
TERM = PREFIX_COLUMN | COLUMNS | QUOTED_STRING | QUOTED_STRING_LIST

COMP_EL = TERM + COMPA_OP + TERM
COMP = Group((PARL + COMP_EL + PARR))
CONDITION = infixNotation(
    COMP,
    [
        (
            NOT,
            1,
            opAssoc.RIGHT,
        ),
        (
            AND,
            2,
            opAssoc.LEFT,
        ),
        (
            OR,
            2,
            opAssoc.LEFT,
        ),
    ],
)
IF_THEN = "if" + CONDITION + "then" + CONDITION
RULE_SYNTAX = IF_THEN | "if () then " + CONDITION | CONDITION


def python_code(expression: str = "", required: list = [], r_type: str = "values"):
    """ """

    regex_condition = re.compile(r"if(.*)then(.*)", re.IGNORECASE)
    rule = regex_condition.search(expression)

    if_part = rule.group(1).strip()
    then_part = rule.group(2).strip()

    python_expressions = {}
    for variable in required:
        if variable == "N":
            if r_type == "values":
                python_expressions[variable] = "len("+DUNDER_DF+".values)"
            else:
                python_expressions[variable] = (DUNDER_DF + "." + r_type
                )
        if variable == "X":
            if r_type == "values":
                if if_part == "()":
                    python_expressions[variable] = "len("+DUNDER_DF+".index)"
                else:
                    python_expressions[variable] = "("+replace_columns(if_part)+").sum()"
            else:
                python_expressions[variable] = (
                    DUNDER_DF + "." + r_type + "[(" + replace_columns(if_part) + ")]"
                )
        elif variable == "~X":
            if r_type == "values":
                python_expressions[variable] = "(~("+replace_columns(if_part)+")).sum()"
            else:
                python_expressions[variable] = (
                    DUNDER_DF + "." + r_type + "[~(" + replace_columns(if_part) + ")]"
                )
        elif variable == "Y":
            if r_type == "values":
                python_expressions[variable] = "("+replace_columns(then_part)+").sum()"
            else:
                python_expressions[variable] = (
                    DUNDER_DF + "." + r_type + "[(" + replace_columns(then_part) + ")]"
                )
        elif variable == "~Y":
            if r_type == "values":
                python_expressions[variable] = "(~("+replace_columns(then_part)+")).sum()"
            else:
                python_expressions[variable] = (
                    DUNDER_DF + "." + r_type + "[~(" + replace_columns(then_part) + ")]"
                )
        elif variable == "X and Y":
            if r_type == "values":
                python_expressions[variable] = "(("+replace_columns(if_part)+") & ("+replace_columns(then_part)+ ")).sum()"
            else:
                python_expressions[variable] = (
                    DUNDER_DF
                    + "."
                    + r_type
                    + "[("
                    + replace_columns(if_part)
                    + ") & ("
                    + replace_columns(then_part)
                    + ")]"
                )
        elif variable == "X and ~Y":
            if r_type == "values":
                python_expressions[variable] = "(("+replace_columns(if_part)+") & ~("+replace_columns(then_part)+ ")).sum()"
            else:
                python_expressions[variable] = (
                    DUNDER_DF
                    + "."
                    + r_type
                    + "[("
                    + replace_columns(if_part)
                    + ") & ~("
                    + replace_columns(then_part)
                    + ")]"
                )
        elif variable == "~X and ~Y":
            if r_type == "values":
                python_expressions[variable] = "(~("+replace_columns(if_part)+") & ~("+replace_columns(then_part)+ ")).sum()"
            else:
                python_expressions[variable] = (
                    DUNDER_DF
                    + "."
                    + r_type
                    + "[~("
                    + replace_columns(if_part)
                    + ") & ~("
                    + replace_columns(then_part)
                    + ")]"
                )
    for e in python_expressions.keys():
        python_expressions[e] = python_expressions[e].replace("[(())]", "")
        python_expressions[e] = python_expressions[e].replace("(()) & ", "")
        python_expressions[e] = python_expressions[e].replace("[~(())]", "[False]")
    return python_expressions


def replace_columns(s: str = ""):
    """Function to replace the column names by a numpy expressions

    Numpy approach:
    {"A"} is rewritten to __df__.values[:, __df__.columns.get_loc("A")]

    Pandas approach:
    {"A"} is rewritten to __df__["A"]

    """
    # return s.replace(
    #     "{", DUNDER_DF + ".values[:, " + DUNDER_DF + ".columns.get_loc("
    # ).replace("}", ")]")
    return s.replace("{", DUNDER_DF + "[").replace("}", "]")


def python_code_for_columns(expression: str = ""):
    """ """
    return {
        "X": (DUNDER_DF + "[(" + replace_columns(expression) + ")]").replace("[()]", "")
    }


def python_code_for_intermediate(expression: str = ""):
    """ """
    return {"X": (replace_columns(expression)).replace("[()]", "")}


def add_brackets(s: str):
    """
    Add brackets around expressions with & and |
    """

    item = re.search(r"(.*)([&|\|])(\s*[(df|df].*)", s)
    if item is not None:
        return (
            "("
            + add_brackets(item.group(1))
            + ") "
            + item.group(2).strip()
            + " ("
            + add_brackets(item.group(3))
            + ")"
        )
    else:
        item = re.search(r"(.*)([>|<|!=|<=|>=|==])(.*)", s)
        if item is not None:
            return (
                add_brackets(item.group(1))
                + item.group(2).strip()
                + add_brackets(item.group(3))
            )
        else:
            return s.strip()


def parenthetic_contents(string):
    """
    Generate parenthesized contents in string as pairs (level, contents).
    """
    stack = []
    if "(" not in string and ")" not in string:
        yield (0, string)
    for i, c in enumerate(string):
        if c == "(":
            stack.append(i)
        elif c == ")" and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1 : i])
