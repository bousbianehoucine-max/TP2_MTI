"""Q12 - Toute la logique du canevas Master 1 GSI (Semestre 1 et Semestre 2).

Lancer:  py main.py
"""

from module import Module
from semester import Semester
from unit import Unit

# Colonnes: code, intitule, coef, credits, C, TD, TP, mode, continu %, examen %
IN, DIST = "In-person", "Distance"

SEMESTER_1 = [
    ("UEF11", "UE fondamentale 11", [
        ("F111", "Réseaux des couches basses",                      3, 6, 1.5, 1.5, 1.5, IN, 40, 60),
        ("F112", "Algorithmique Avancée et Complexité",             2, 4, 1.5, 0,   1.5, IN, 40, 60),
    ]),
    ("UEF12", "UE fondamentale 12", [
        ("F121", "Système d'exploitation",                          2, 4, 1.5, 1.5, 0,   IN, 40, 60),
        ("F122", "Architectures Modernes des Systèmes Informatiques", 2, 4, 1.5, 0, 1.5, IN, 40, 60),
    ]),
    ("UEM11", "UE Méthodologie", [
        ("M111", "Architecture et administration des bases de données", 2, 4, 1.5, 0, 1.5, IN, 40, 60),
        ("M112", "Méthodes et Technologies d'Implémentation",       3, 5, 1.5, 0,   1.5, IN, 40, 60),
    ]),
    ("UED11", "UE Découverte", [
        ("D111", "Systèmes de Communication Vocaux et Vidéos",      2, 2, 1.5, 0,   1.5, IN, 40, 60),
    ]),
    ("UET11", "UE Transversale", [
        ("T111", "Cloud Computing",                                 1, 1, 1.5, 0,   0,   DIST, 0, 100),
    ]),
]

SEMESTER_2 = [
    ("UEF21", "UE fondamentale 21", [
        ("F211", "Les Middlewares pour les systèmes répartis",      3, 6, 1.5, 1.5, 1.5, IN, 40, 60),
        ("F212", "Modélisation et Architectures logicielles",       2, 4, 1.5, 0,   1.5, IN, 40, 60),
    ]),
    ("UEF22", "UE fondamentale 22", [
        ("F221", "Réseaux de la couche IP",                         3, 6, 1.5, 0,   1.5, IN, 40, 60),
        ("F222", "Introduction au Machine Learning",                2, 4, 1.5, 0,   1.5, IN, 40, 60),
    ]),
    ("UEM21", "UE Méthodologique", [
        ("M211", "Infographie",                                     2, 3, 1.5, 0,   1.5, IN, 40, 60),
        ("M212", "Gestion de l'incertain",                          2, 3, 1.5, 1.5, 0,   IN, 40, 60),
    ]),
    ("UED21", "UE Découverte", [
        ("D211", "Internet of Things",                              2, 3, 1.5, 0,   1.5, IN, 40, 60),
    ]),
    ("UET21", "UE Transversale", [
        ("T211", "Cybercriminalité",                                1, 1, 1.5, 0,   0,   DIST, 0, 100),
    ]),
]


def _build(name, title, table):
    """Construit un NOUVEL arbre Semester -> Unit -> Module (donc des notes vierges)."""
    semester = Semester(name, title)
    for unit_code, unit_title, rows in table:
        unit = Unit(unit_code, unit_title)
        for (code, mod_title, coef, credit, c, td, tp, mode, cont, exam) in rows:
            unit.add_module(Module(code, mod_title, coef=coef, credit=credit,
                                   hours_lecture=c, hours_td=td, hours_tp=tp,
                                   teaching_mode=mode,
                                   continous_percent=cont, exam_percent=exam))
        semester.add_unit(unit)
    return semester


def build_semester1():
    return _build("S1", "Semestre 1", SEMESTER_1)


def build_semester2():
    return _build("S2", "Semestre 2", SEMESTER_2)


def apply_grades(semester, grades):
    """grades = {"F111": {"tp": 12, "td": 10, "exam": 9}, ...}"""
    for code, marks in grades.items():
        semester.get_module(code).set_grade(**marks)


def print_report(student, semester):
    print(f"\n=== {student} - {semester.title} ===")
    for unit in semester.units:
        print(f"{unit.name} ({unit.title}): moyenne {unit.calculate_average():.2f}"
              f" | credits {unit.calculate_credits()}/{unit.credit}")
        for m in unit.modules:
            print(f"    {m.name:<5} {m.title[:40]:<40} moy {m.calculate_average():5.2f}"
                  f" | credits {m.calculate_credits()}/{m.credit}")
    verdict = "VALIDE" if semester.calculate_credits() == semester.credit else "NON VALIDE"
    print(f"--> Moyenne du semestre: {semester.calculate_average():.2f}"
          f" | credits {semester.calculate_credits()}/{semester.credit}  [{verdict}]")


if __name__ == "__main__":
    s1 = build_semester1()
    print(f"{s1.title}: coef total {s1.coef}, credits {s1.credit}, VHS {s1.total_hours} h")
    s2 = build_semester2()
    print(f"{s2.title}: coef total {s2.coef}, credits {s2.credit}, VHS {s2.total_hours} h")

    # Etudiante 1: bons resultats
    student1 = build_semester1()
    apply_grades(student1, {
        "F111": {"tp": 14, "td": 12, "exam": 13}, "F112": {"tp": 13, "exam": 12},
        "F121": {"td": 11, "exam": 10},           "F122": {"tp": 15, "exam": 11},
        "M111": {"tp": 12, "exam": 10},           "M112": {"tp": 16, "exam": 14},
        "D111": {"tp": 14, "exam": 12},           "T111": {"exam": 15},
    })
    print_report("Etudiante A", student1)

    # Etudiante 2: moyenne < 10 -> credits partiels (module par module)
    student2 = build_semester1()
    apply_grades(student2, {
        "F111": {"tp": 8, "td": 7, "exam": 6},    "F112": {"tp": 9, "exam": 7},
        "F121": {"td": 12, "exam": 11},           "F122": {"tp": 10, "exam": 9},
        "M111": {"tp": 11, "exam": 12},           "M112": {"tp": 13, "exam": 8},
        "D111": {"tp": 10, "exam": 10},           "T111": {"exam": 14},
    })
    print_report("Etudiante B", student2)

