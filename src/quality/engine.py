from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from .rule import Rule, RuleResult


class Engine:
    """Ejecutor de reglas sobre uno o más archivos."""

    def __init__(self, rules: Iterable[Rule]) -> None:
        self.rules = list(rules)

    @staticmethod
    def read_lines(path: Path) -> List[str]:
        return path.read_text(encoding="utf-8").splitlines(keepends=False)

    def run_on_file(self, path: Path) -> list[tuple[str, RuleResult]]:
        lines = self.read_lines(path)
        results: list[tuple[str, RuleResult]] = []
        for rule in self.rules:
            results.append((rule.name, rule.check(lines)))
        return results
