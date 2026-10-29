"""Q8, Q11 - Classe Semester (semestre = ensemble d'unites)."""

from academicelement import AcademicElement


class Semester(AcademicElement):
    """Represents a semester containing several teaching units."""

    def __init__(self, name, title, units=None):
        super().__init__(name, title)
        self._units = []
        for unit in units or []:
            self.add_unit(unit)

    @property
    def units(self):
        return tuple(self._units)

    def add_unit(self, unit):
        self._units.append(unit)
        self._refresh_totals()

    def _refresh_totals(self):
        self.coef = sum(u.coef for u in self._units)
        self.credit = sum(u.credit for u in self._units)
        self.hours_lecture = sum(u.hours_lecture for u in self._units)
        self.hours_td = sum(u.hours_td for u in self._units)
        self.hours_tp = sum(u.hours_tp for u in self._units)

    # ---------------- Parcours de l'arbre Semester -> Unit -> Module ----------------
    def all_modules(self):
        return [m for u in self._units for m in u.modules]

    def get_module(self, code):
        for module in self.all_modules():
            if module.name == code:
                return module
        raise KeyError(f"Unknown module code: {code}")

    # ---------------- Calculs ----------------
    def calculate_average(self):
        """Moyenne ponderee des UE par leur coefficient (somme des coef. des modules)."""
        if not self._units:
            return 0
        total = sum(u.calculate_average() * u.coef for u in self._units)
        coef_sum = sum(u.coef for u in self._units)
        return total / coef_sum

    def calculate_credits(self):
        """Moyenne semestre >= 10: les 30 credits (compensation entre UE).
        Sinon: somme des credits acquis dans chaque UE."""
        if not self._units:
            return 0
        if self.calculate_average() >= self.PASS_MARK:
            return sum(u.credit for u in self._units)
        return sum(u.calculate_credits() for u in self._units)

