import pytest

from academicelement import AcademicElement
from module import Module


def make_mti():
    return Module("MTI", "Methods & Technologies of Implementation",
                  coef=3, credit=5, hours_tp=1.5,
                  continous_percent=40, exam_percent=60)


def test_total_hours():
    assert make_mti().total_hours == 15 * (1.5 + 0 + 1.5) # 45


def test_average_tp_and_exam():
    m = make_mti()
    m.set_grade(tp=10, exam=12)
    assert m.calculate_average() == pytest.approx(10 * 0.4 + 12 * 0.6) # 11.2


def test_average_with_td_and_tp_shares_continuous():
    m = Module("F111", "Reseaux", coef=3, credit=6,
               hours_td=1.5, hours_tp=1.5) # 20% TD + 20% TP + 60% examen
    m.set_grade(tp=10, td=20, exam=10)
    assert m.calculate_average() == pytest.approx(2 + 4 + 6)


def test_exam_only_module():
    m = Module("T111", "Cloud", coef=1, credit=1, teaching_mode="Distance",
               continous_percent=0, exam_percent=100)
    m.set_grade(exam=15)
    assert m.calculate_average() == 15


def test_credits_validated_only_if_average_ge_10():
    m = make_mti()
    m.set_grade(tp=10, exam=10)
    assert m.calculate_credits() == 5
    m.set_grade(tp=8, exam=6)
    assert m.calculate_credits() == 0


def test_default_grades_do_not_crash():
    assert make_mti().calculate_average() == 0


def test_invalid_grade_rejected():
    with pytest.raises(ValueError):
        make_mti().set_grade(exam=25)


def test_invalid_percentages_rejected():
    with pytest.raises(ValueError):
        Module("X", "bad", continous_percent=50, exam_percent=60)


def test_grades_are_encapsulated():
    m = make_mti()
    m.get_grades()["exam"] = 20 # modifie une copie seulement
    assert m.get_grades()["exam"] == 0


def test_academic_element_is_abstract():
    with pytest.raises(TypeError):
        AcademicElement("x", "y")

