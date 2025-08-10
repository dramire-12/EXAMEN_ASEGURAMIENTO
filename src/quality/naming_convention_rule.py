from __future__ import annotations

import re
from typing import Any, Dict, List

from .interfaces import Reportable, Serializable
from .rule import Rule, RuleResult


class NamingConventionRule(Rule, Serializable, Reportable):
    """
    Verifica que las funciones se definan en snake_case: def mi_funcion():
    """

    name = "naming-convention"

    def __init__(self) -> None:
        self._last_result: RuleResult | None = None

    def check(self, lines: List[str]) -> RuleResult:
        pattern = re.compile(r"^\s*def\s+([a-z_][a-z0-9_]*)\s*\(", re.IGNORECASE)
        bad: List[str] = []

        for i, line in enumerate(lines, start=1):
            if line.strip().startswith("def "):
                # Extrae el nombre y verifica que esté en snake_case estricto
                m = pattern.match(line)
                if not m or m.group(1) != m.group(1).lower() or "__" in m.group(1):
                    bad.append(f"Línea {i}: Nombre de función no cumple snake_case -> {line.strip()}")

        result = RuleResult(passed=len(bad) == 0, messages=bad or ["OK"])
        self._last_result = result
        return result

    # Interfaces
    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule": self.name,
            "passed": None if self._last_result is None else self._last_result.passed,
            "messages": None if self._last_result is None else self._last_result.messages,
        }

    def report(self) -> str:
        if self._last_result is None:
            return f"[{self.name}] Aún no evaluada."
        status = "PASÓ" * self._last_result.passed or "FALLÓ"
        details = "\n".join(self._last_result.messages)
        return f"[{self.name}] {status}\n{details}"
