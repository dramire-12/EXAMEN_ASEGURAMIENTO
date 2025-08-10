from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class RuleResult:
    passed: bool
    messages: List[str]


class Rule(ABC):
    """Clase abstracta: una regla de calidad que se puede evaluar sobre líneas de código."""

    name: str = "generic-rule"

    @abstractmethod
    def check(self, lines: list[str]) -> RuleResult:
        """Evalúa la regla y retorna RuleResult."""
