from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List

from .engine import Engine
from .repository import EvaluationRecord, RuleResultRepository


class QualityService:
    """Orquesta la evaluación de archivos y persiste resultados."""

    def __init__(self, engine: Engine, repo: RuleResultRepository) -> None:
        self.engine = engine
        self.repo = repo

    def evaluate_file(self, path: Path) -> List[EvaluationRecord]:
        """Evalúa un archivo con todas las reglas y guarda registros."""
        results = self.engine.run_on_file(path)
        now = datetime.now()
        records: List[EvaluationRecord] = []

        for rule_name, result in results:
            records.append(
                EvaluationRecord(
                    file=str(path),
                    rule=rule_name,
                    passed=result.passed,
                    messages=result.messages,
                    at=now,
                )
            )

        self.repo.save_many(records)
        return records

    def history_for(self, path: Path) -> List[EvaluationRecord]:
        """Devuelve historial de evaluaciones para un archivo."""
        return self.repo.list_by_file(str(path))
