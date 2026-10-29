"""
ПЗ №3. Учёт инцидентов информационной безопасности.
Демонстрация наследования, полиморфизма, магических методов,
пользовательских исключений и класса-контейнера.
Python 3.10+
"""
from __future__ import annotations

from datetime import datetime
from typing import Iterable, Iterator


class IncidentError(Exception):
    """Базовое исключение предметной области инцидентов."""


class InvalidIncidentError(IncidentError):
    """Ошибка при создании или изменении некорректного инцидента."""


class IncidentNotFoundError(IncidentError):
    """Инцидент с указанным идентификатором не найден."""


class Incident:
    """Базовый класс инцидента информационной безопасности."""

    DEFAULT_RISK_WEIGHT = 1.0

    def __init__(
        self,
        incident_id: str,
        title: str,
        severity: int,
        status: str = "Открыт",
        created_at: datetime | None = None,
    ) -> None:
        incident_id = str(incident_id).strip()
        title = str(title).strip()
        if not incident_id:
            raise InvalidIncidentError("Идентификатор инцидента не может быть пустым.")
        if not title:
            raise InvalidIncidentError("Название инцидента не может быть пустым.")
        if not isinstance(severity, int) or not 1 <= severity <= 5:
            raise InvalidIncidentError("Критичность должна быть целым числом от 1 до 5.")
        if status not in {"Открыт", "В работе", "Закрыт"}:
            raise InvalidIncidentError(
                "Статус должен быть одним из: Открыт, В работе, Закрыт."
            )

        self.incident_id = incident_id
        self.title = title
        self.severity = severity
        self.status = status
        self.created_at = created_at or datetime.now()

    def calculate_risk(self) -> float:
        """Полиморфный метод: базовый класс задаёт общий интерфейс."""
        raise NotImplementedError("Метод calculate_risk() должен быть переопределён.")

    def close(self) -> None:
        self.status = "Закрыт"

    def __str__(self) -> str:
        return (
            f"[{self.incident_id}] {self.title} | критичность: {self.severity}/5"
            f" | статус: {self.status} | риск: {self.calculate_risk():.1f}"
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(incident_id={self.incident_id!r}, "
            f"title={self.title!r}, severity={self.severity!r}, "
            f"status={self.status!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Incident):
            return NotImplemented
        return self.incident_id == other.incident_id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Incident):
            return NotImplemented
        return (self.calculate_risk(), self.incident_id) < (
            other.calculate_risk(), other.incident_id
        )

    def __add__(self, other: object) -> float:
        """Суммарный риск двух инцидентов."""
        if not isinstance(other, Incident):
            return NotImplemented
        return self.calculate_risk() + other.calculate_risk()


class MalwareIncident(Incident):
    """Инцидент, связанный с вредоносным ПО."""

    DEFAULT_RISK_WEIGHT = 1.8

    def calculate_risk(self) -> float:
        # Вредоносное ПО может быстро распространяться, поэтому вес повышен.
        status_factor = 0.5 if self.status == "Закрыт" else 1.0
        return self.severity * self.DEFAULT_RISK_WEIGHT * status_factor


class DataLeakIncident(Incident):
    """Инцидент, связанный с утечкой данных."""

    DEFAULT_RISK_WEIGHT = 2.2

    def calculate_risk(self) -> float:
        status_factor = 0.5 if self.status == "Закрыт" else 1.0
        return self.severity * self.DEFAULT_RISK_WEIGHT * status_factor


class IncidentRegistry:
    """Контейнер для хранения и поиска инцидентов."""

    def __init__(self, incidents: Iterable[Incident] | None = None) -> None:
        self._incidents: list[Incident] = []
        for incident in incidents or []:
            self.add(incident)

    def add(self, incident: Incident) -> None:
        if not isinstance(incident, Incident):
            raise InvalidIncidentError("В реестр можно добавлять только объекты Incident.")
        if incident in self._incidents:
            raise InvalidIncidentError(
                f"Инцидент с ID {incident.incident_id!r} уже зарегистрирован."
            )
        self._incidents.append(incident)

    def get_by_id(self, incident_id: str) -> Incident:
        for incident in self._incidents:
            if incident.incident_id == incident_id:
                return incident
        raise IncidentNotFoundError(f"Инцидент с ID {incident_id!r} не найден.")

    def sorted_by_risk(self, descending: bool = True) -> list[Incident]:
        return sorted(self._incidents, reverse=descending)

    def __len__(self) -> int:
        return len(self._incidents)

    def __getitem__(self, index: int | slice) -> Incident | list[Incident]:
        return self._incidents[index]

    def __iter__(self) -> Iterator[Incident]:
        return iter(self._incidents)

    def __str__(self) -> str:
        return f"Реестр инцидентов: {len(self)} записей"

    def __repr__(self) -> str:
        return f"IncidentRegistry({self._incidents!r})"


def main() -> None:
    print("=== Система учёта инцидентов ИБ ===")
    registry = IncidentRegistry()

    malware = MalwareIncident("IB-001", "Обнаружено вредоносное ПО", 4)
    leak = DataLeakIncident("IB-002", "Подозрение на утечку данных", 5)
    registry.add(malware)
    registry.add(leak)

    print(f"\n{registry}")
    print("\nИсходный список:")
    for incident in registry:
        print(incident)

    print("\nСортировка по риску (от высокого к низкому):")
    for incident in registry.sorted_by_risk():
        print(incident)

    print("\nПолиморфный расчёт риска:")
    for incident in registry:
        print(f"{type(incident).__name__}: риск = {incident.calculate_risk():.1f}")

    print(f"\nlen(registry) = {len(registry)}")
    print(f"registry[0] = {registry[0]}")
    print(f"repr(malware) = {malware!r}")
    print(f"malware == MalwareIncident с тем же ID: "
          f"{malware == MalwareIncident('IB-001', 'Дубликат для сравнения', 1)}")
    print(f"Суммарный риск двух инцидентов (malware + leak): {malware + leak:.1f}")

    print("\nДемонстрация обработки пользовательских исключений:")
    try:
        registry.add(MalwareIncident("IB-001", "Повторный ID", 2))
    except InvalidIncidentError as error:
        print(f"Перехвачено InvalidIncidentError: {error}")

    try:
        registry.get_by_id("IB-999")
    except IncidentNotFoundError as error:
        print(f"Перехвачено IncidentNotFoundError: {error}")

    try:
        MalwareIncident("IB-003", "Некорректная критичность", 9)
    except InvalidIncidentError as error:
        print(f"Перехвачено InvalidIncidentError: {error}")

    print("\nРабота программы завершена.")


if __name__ == "__main__":
    main()
