from polars import Expr, all_horizontal, any_horizontal
from polars import when, Int8, Boolean


def and_(a: Expr, b: Expr, *args) -> Expr:
    """Logical AND operator, returns true if both operands are true and returns false otherwise"""
    return all_horizontal(a, b, *args)


def equal(input1: Expr, input2: Expr) -> Expr:
    """Returns true if both inputs are same and returns false otherwise"""
    return input1 == input2


def if_else(input1: Expr, input2: Expr, input3: Expr = None) -> Expr:
    """If input1 is true then return input2 else return input3."""
    return when(input1).then(input2).otherwise(input3)


def is_finite(input1: Expr) -> Expr:
    """If (input NaN or input == INF) return 0, else return 1"""
    return input1.is_finite()


def is_nan(input1: Expr) -> Expr:
    """If (input == NaN) return 1 else return 0"""
    return input1.is_nan()


def is_not_finite(input1: Expr) -> Expr:
    """If (input NAN or input == INF) return 1 else return 0"""
    return input1.is_infinite()


def is_not_nan(input1: Expr) -> Expr:
    """If (input != NaN) return 1 else return 0"""
    return input1.is_not_nan()


def less(input1: Expr, input2: Expr) -> Expr:
    """If input1 < input2 return true, else return false"""
    return input1 < input2


def negate(input1: Expr) -> Expr:
    """The result is true if the converted operand is false; the result is false if the converted operand is true"""
    return ~input1


def or_(a: Expr, b: Expr, *args) -> Expr:
    """Logical OR operator returns true if either or both inputs are true and returns false otherwise"""
    return any_horizontal(a, b, *args)


def xor(a: Expr, b: Expr) -> Expr:
    """Logical XOR operator returns true if exactly one of the inputs is true and returns false otherwise"""
    return a.xor(b)


def int_(a: Expr) -> Expr:
    """convert bool to int"""
    return a.cast(Int8)


def bool_(a: Expr) -> Expr:
    """convert int to bool"""
    return a.cast(Boolean)
