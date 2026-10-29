"""Q7 - Classe abstraite commune a Module, Unit et Semester."""

from abc import ABC, abstractmethod


class AcademicElement(ABC):
    """Abstract base class for academic entities (Module, Unit, Semester, etc.).

    Correction par rapport au sujet: on herite de ABC.
    Sans ABC, @abstractmethod n'est PAS verifie par Python et on pourrait
    creer AcademicElement("x", "y") sans erreur.
    """

    PASS_MARK = 10          # moyenne minimale pour valider (sur 20)

    def __init__(self, name, title):
        self.name = name
        self.title = title
        self._WEEKS = 15            # Encapsulation: attribut "prive" (convention _)
        self.coef = 0
        self.credit = 0

        # Workload distribution (volume horaire hebdomadaire)
        self.hours_lecture = 0
        self.hours_td = 0
        self.hours_tp = 0

    @property
    def total_hours(self):
        """VHS sur le semestre. Propriete: toujours a jour si les heures changent."""
        return self._WEEKS * (self.hours_lecture + self.hours_td + self.hours_tp)

    @abstractmethod
    def calculate_average(self):
        """Abstract method to be implemented by subclasses."""

