import pytest

from main import apply_grades, build_semester1, build_semester2
from semester import Semester


def test_canvas_totals_semester_1():
    s1 = build_semester1()
    assert s1.coef == 17
    assert s1.credit == 30
    assert s1.total_hours == 360
    assert (s1.hours_lecture, s1.hours_td, s1.hours_tp) == (12, 3, 9)


def test_canvas_totals_semester_2():
    s2 = build_semester2()
    assert s2.coef == 17
    assert s2.credit == 30
    assert s2.total_hours == 360
    assert (s2.hours_lecture, s2.hours_td, s2.hours_tp) == (12, 3, 9)


def test_module_hours_match_canvas():
    s1 = build_semester1()
    assert s1.get_module("F111").total_hours == 67.5
    assert s1.get_module("F112").total_hours == 45
    assert s1.get_module("T111").total_hours == 22.5


def test_semester_average_equals_coef_weighted_average_of_all_modules():
    s1 = build_semester1()
    apply_grades(s1, {
        "F111": {"tp": 14, "td": 12, "exam": 13}, "F112": {"tp": 13, "exam": 12},
        "F121": {"td": 11, "exam": 10},           "F122": {"tp": 15, "exam": 11},
        "M111": {"tp": 12, "exam": 10},           "M112": {"tp": 16, "exam": 14},
        "D111": {"tp": 14, "exam": 12},           "T111": {"exam": 15},
    })
    mods = s1.all_modules()
    expected = sum(m.calculate_average() * m.coef for m in mods) / sum(m.coef for m in mods)
    assert s1.calculate_average() == pytest.approx(expected)
    assert s1.calculate_credits() == 30


def test_semester_below_10_gives_partial_credits():
    s1 = build_semester1()
    apply_grades(s1, {
        "F111": {"tp": 8, "td": 7, "exam": 6},    "F112": {"tp": 9, "exam": 7},
        "F121": {"td": 12, "exam": 11},           "F122": {"tp": 10, "exam": 9},
        "M111": {"tp": 11, "exam": 12},           "M112": {"tp": 13, "exam": 8},
        "D111": {"tp": 10, "exam": 10},           "T111": {"exam": 14},
    })
    assert s1.calculate_average() < 10
    assert s1.calculate_credits() == 20


def test_unknown_module_code():
    with pytest.raises(KeyError):
        build_semester1().get_module("XXXX")


def test_empty_semester():
    s = Semester("S", "empty")
    assert s.calculate_average() == 0
    assert s.calculate_credits() == 0

