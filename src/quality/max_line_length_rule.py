from __future__ import annotations

from typing import Any, Dict, List

from .interfaces import Reportable, Serializable
from .rule import Rule, RuleResult


class MaxLineLengthRule(Rule, Serializable, Reportable):
    """Verifica que ninguna línea exceda un largo máximo."""

    name = "max-line-length"

    def __init__(self, max_len: int = 100) -> None:
        self.max_len = max_len
        self._last_result: RuleResult | None = None

    def check(self, lines: List[str]) -> RuleResult:
        bad: List[str] = []
        for i, line in enumerate(lines, start=1):
            if len(line.rstrip("\n")) > self.max_len:
                bad.append(f"Línea {i}: {len(line.rstrip())} caracteres (máx {self.max_len})")

        result = RuleResult(passed=len(bad) == 0, messages=bad or ["OK"])
        self._last_result = result
        return result

    # Interfaces
    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule": self.name,
            "config": {"max_len": self.max_len},
            "passed": None if self._last_result is None else self._last_result.passed,
            "messages": None if self._last_result is None else self._last_result.messages,
        }

    def report(self) -> str:
        if self._last_result is None:
            return f"[{self.name}] Aún no evaluada."
        status = "PASÓ" * self._last_result.passed or "FALLÓ"
        details = "\n".join(self._last_result.messages)
        return f"[{self.name}] {status}\n{details}"
