from typing import Protocol


class Exporter(Protocol):
    def export(self, rows) -> list: ...


class ListExporter:
    def export(self, rows):
        return list(rows)
