from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List


@dataclass(frozen=True)
class EvaluationRecord:
    file: str
    rule: str
    passed: bool
    messages: List[str]
    at: datetime


class RuleResultRepository(ABC):
    """Contrato de repositorio para persistir resultados de reglas."""

    @abstractmethod
    def save(self, record: EvaluationRecord) -> None: ...

    @abstractmethod
    def save_many(self, records: Iterable[EvaluationRecord]) -> None: ...

    @abstractmethod
    def list_all(self) -> List[EvaluationRecord]: ...

    @abstractmethod
    def list_by_file(self, file: str) -> List[EvaluationRecord]: ...

    @abstractmethod
    def clear(self) -> None: ...


class InMemoryRuleResultRepository(RuleResultRepository):
    """Implementación simple en memoria (ideal para pruebas)."""

    def __init__(self) -> None:
        self._data: List[EvaluationRecord] = []

    def save(self, record: EvaluationRecord) -> None:
        self._data.append(record)

    def save_many(self, records: Iterable[EvaluationRecord]) -> None:
        self._data.extend(records)

    def list_all(self) -> List[EvaluationRecord]:
        return list(self._data)

    def list_by_file(self, file: str) -> List[EvaluationRecord]:
        return [r for r in self._data if r.file == file]

    def clear(self) -> None:
        self._data.clear()
