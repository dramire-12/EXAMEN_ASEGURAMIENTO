
## `src/quality/interfaces.py`  *(2 interfaces con ABC)*

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class Serializable(ABC):
    """Interface: objetos que pueden serializar su estado a dict."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serializa a diccionario."""


class Reportable(ABC):
    """Interface: objetos que generan un reporte de texto."""

    @abstractmethod
    def report(self) -> str:
        """Devuelve un reporte legible."""
