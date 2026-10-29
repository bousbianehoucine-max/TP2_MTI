"""Q2, Q3, Q7, Q9 - Classe Module."""

from academicelement import AcademicElement


class Module(AcademicElement):
    """Represents a teaching module with pedagogical and evaluation attributes."""

    def __init__(
        self,
        name: str = "",              # module code
        title: str = "",
        coef: int = 1,
        credit: int = 1,
        hours_lecture: float = 1.5,
        hours_td: float = 0,
        hours_tp: float = 0,
        teaching_mode: str = "In-person",   # "Distance" or "In-person"
        continous_percent: int = 40,
        exam_percent: int = 60,
    ):
        super().__init__(name, title)

        # Q9: validation (on refuse un module incoherent)
        if continous_percent + exam_percent != 100:
            raise ValueError("continous_percent + exam_percent must be 100")

        self.coef = coef
        self.credit = credit

        # Workload distribution (volume horaire)
        self.hours_lecture = hours_lecture
        self.hours_td = hours_td
        self.hours_tp = hours_tp

        # Teaching and evaluation mode
        self.teaching_mode = teaching_mode
        self.evaluation_continous_percent = continous_percent
        self.evaluation_exam_percent = exam_percent

        # Q7: notes a 0 au depart (avec None, calculate_average plante: None * float)
        self._grades = {"tp": 0, "td": 0, "exam": 0}

    # ---------------- Encapsulation: acces controle aux notes ----------------
    @staticmethod
    def _check_grade(value):
        if not 0 <= value <= 20:
            raise ValueError(f"A grade must be between 0 and 20, got {value}")

    def set_grade(self, tp=None, td=None, exam=None):
        for key, value in (("tp", tp), ("td", td), ("exam", exam)):
            if value is not None:
                self._check_grade(value)
                self._grades[key] = value

    def get_grades(self):
        """Lecture seule: on renvoie une COPIE, pas le dictionnaire interne."""
        return dict(self._grades)

    # ---------------- Description ----------------
    def summary(self):
        """Return a short textual description of the module."""
        return (
            f"Module: {self.title} ({self.name})\n"
            f"Coefficient: {self.coef}, Credits: {self.credit}\n"
            f"Hours: total {self.total_hours}, {self.hours_lecture} Lecture, "
            f"{self.hours_td} TD, {self.hours_tp} TP\n"
            f"Teaching mode: {self.teaching_mode}, "
            f"Evaluation mode: Continous: {self.evaluation_continous_percent}% "
            f"Exam: {self.evaluation_exam_percent}% "
        )

    # ---------------- Q3: calculs ----------------
    def calculate_average(self):
        """Polymorphism: different modules could override this behavior."""
        tp = self._grades["tp"]
        td = self._grades["td"]
        exam = self._grades["exam"]
        percent_exam = self.evaluation_exam_percent
        percent_tp = percent_td = 0
        if self.hours_tp and self.hours_td:         # TD et TP: le continu est partage
            percent_tp = percent_td = self.evaluation_continous_percent / 2
        elif self.hours_td:
            percent_td = self.evaluation_continous_percent
        elif self.hours_tp:
            percent_tp = self.evaluation_continous_percent
        return (
            tp * percent_tp / 100
            + td * percent_td / 100
            + exam * percent_exam / 100
        )

    def calculate_credits(self):
        """Polymorphism: different modules could override this behavior."""
        if self.calculate_average() >= self.PASS_MARK:
            return self.credit
        return 0


# Example usage
if __name__ == "__main__":
    mti = Module(
        name="MTI",
        title="Methods and Technologies of Implementation",
        coef=3,
        credit=5,
        hours_lecture=1.5,
        hours_tp=1.5,
        teaching_mode="In-person",
    )
    print(mti.summary())
    mti.set_grade(tp=10, exam=12)
    print("Module average:", mti.name, mti.calculate_average())

