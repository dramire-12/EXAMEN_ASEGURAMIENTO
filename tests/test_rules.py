from src.quality.max_line_length_rule import MaxLineLengthRule
from src.quality.naming_convention_rule import NamingConventionRule


def test_max_line_length_rule_ok():
    rule = MaxLineLengthRule(max_len=10)
    res = rule.check(["short", "lines"])
    assert res.passed is True


def test_max_line_length_rule_fail():
    rule = MaxLineLengthRule(max_len=5)
    res = rule.check(["123456"])
    assert res.passed is False
    assert "Línea 1" in res.messages[0]


def test_naming_convention_rule_ok():
    rule = NamingConventionRule()
    res = rule.check(["def mi_funcion():", "    pass"])
    assert res.passed is True


def test_naming_convention_rule_fail():
    rule = NamingConventionRule()
    res = rule.check(["def MiFuncion():", "    pass"])
    assert res.passed is False
