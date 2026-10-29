"""Q4, Q10 - Classe Unit (unite d'enseignement = ensemble de modules)."""

from academicelement import AcademicElement


class Unit(AcademicElement):
    """Represents a teaching unit containing multiple modules."""

    def __init__(self, name, title, modules=None):
        super().__init__(name, title)
        # Correction: le sujet ecrit modules=[] -> UNE SEULE liste partagee par
        # tous les objets Unit (piege classique de Python). On utilise None.
        self._modules = []
        for module in modules or []:
            self.add_module(module)

    @property
    def modules(self):
        return tuple(self._modules)          # lecture seule

    def add_module(self, module):
        self._modules.append(module)
        self._refresh_totals()

    def _refresh_totals(self):
        """Une UE a pour coef/credits/heures la SOMME de ses modules."""
        self.coef = sum(m.coef for m in self._modules)
        self.credit = sum(m.credit for m in self._modules)
        self.hours_lecture = sum(m.hours_lecture for m in self._modules)
        self.hours_td = sum(m.hours_td for m in self._modules)
        self.hours_tp = sum(m.hours_tp for m in self._modules)

    # ---------------- Q10: Override ----------------
    def calculate_average(self):
        """Example of aggregation - combining module averages (ponderee par coef)."""
        if not self._modules:
            return 0
        total = sum(m.calculate_average() * m.coef for m in self._modules)
        coef_sum = sum(m.coef for m in self._modules)
        return total / coef_sum

    def calculate_credits(self):
        """Moyenne UE >= 10: tous les credits (compensation entre modules).
        Sinon: seulement les credits des modules valides individuellement."""
        if not self._modules:
            return 0
        if self.calculate_average() >= self.PASS_MARK:
            return sum(m.credit for m in self._modules)
        return sum(m.calculate_credits() for m in self._modules)

