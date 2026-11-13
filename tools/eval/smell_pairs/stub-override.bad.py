class Exporter:
    def export(self, rows):
        return list(rows)


class NullExporter(Exporter):
    def export(self, rows):
        raise NotImplementedError
