import pytest

from module import Module
from unit import Unit


def two_modules():
    m1 = Module("MTI", "Methods", coef=3, credit=5, hours_tp=1.5)
    m2 = Module("AABD", "Database", coef=2, credit=4, hours_tp=1.5)
    return m1, m2


def test_unit_totals_are_sums():
    m1, m2 = two_modules()
    u = Unit("UEM11", "UE Methodologie", [m1, m2])
    assert u.coef == 5
    assert u.credit == 9
    assert u.total_hours == 15 * 6


def test_unit_average_is_weighted_by_coef():
    m1, m2 = two_modules()
    m1.set_grade(tp=10, exam=12)          # 11.2
    m2.set_grade(tp=8, exam=6)            # 6.8
    u = Unit("UEM11", "UE Methodologie", [m1, m2])
    assert u.calculate_average() == pytest.approx((11.2 * 3 + 6.8 * 2) / 5)


def test_unit_compensation_gives_all_credits():
    m1, m2 = two_modules()
    m1.set_grade(tp=16, exam=16)          # 16
    m2.set_grade(tp=6, exam=6)            # 6  -> moyenne UE = 12 >= 10
    u = Unit("UEM11", "UE", [m1, m2])
    assert u.calculate_credits() == 9


def test_unit_below_10_gives_only_validated_modules():
    m1, m2 = two_modules()
    m1.set_grade(tp=11, exam=11)          # 11 valide
    m2.set_grade(tp=2, exam=2)            # 2
    u = Unit("UEM11", "UE", [m1, m2])
    assert u.calculate_average() < 10
    assert u.calculate_credits() == 5


def test_empty_unit():
    u = Unit("U", "empty")
    assert u.calculate_average() == 0
    assert u.calculate_credits() == 0


def test_units_do_not_share_module_list():
    """Verifie la correction du piege modules=[] du sujet."""
    u1, u2 = Unit("A", "a"), Unit("B", "b")
    u1.add_module(Module("M1", "m1"))
    assert len(u2.modules) == 0

