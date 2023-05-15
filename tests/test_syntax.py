import pytest
from project.Lagraph.utils import is_valid_syntax


def test_empty():
    assert is_valid_syntax("")
    assert is_valid_syntax("--simple comment")


def not_statement():
    assert not is_valid_syntax("\\ abc -> 12")


def test_bind():
    assert is_valid_syntax("let x = 12")
    assert is_valid_syntax('let x = "abcd"')


def test_expr():
    assert is_valid_syntax("print 12")
    assert is_valid_syntax('print "abc\'!\_d"')
    assert is_valid_syntax("print setStart 1 to x1")
    assert is_valid_syntax("print setFinal 1 to x1")
    assert is_valid_syntax("print addStart 1 to x1")
    assert is_valid_syntax("print addFinal 1 to x1")
    assert is_valid_syntax("print startOf x1")
    assert is_valid_syntax("print finalOf x1")
    assert is_valid_syntax("print reachableOf x1")
    assert is_valid_syntax("print verticesOf x1")
    assert is_valid_syntax("print edgesOf x1")
    assert is_valid_syntax("print labelsOf x1")
    assert is_valid_syntax('print load path "\\home\\graphs\\a.dot"')
    assert is_valid_syntax('print load graph "a -> b -> c"')
    assert is_valid_syntax("print a && a")
    assert is_valid_syntax("print a || b")
    assert is_valid_syntax("print a ++ b")
    assert is_valid_syntax("print a || b")
    assert is_valid_syntax("print a*")
    assert is_valid_syntax('print a || ((1 ++ 2) && "aaaa")')


def test_bad_expr():
    assert not is_valid_syntax('print load griph "a -> b -> c"')
    assert not is_valid_syntax('print load puth "a -> b -> c"')
    assert not is_valid_syntax("print a & a")
    assert not is_valid_syntax("print a | b")
    assert not is_valid_syntax("print a + b")
    assert not is_valid_syntax("print a | b")
    assert not is_valid_syntax("print a ** b")
    assert not is_valid_syntax("print a * b")
