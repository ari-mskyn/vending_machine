class MockDBTable:
    def __init__(self, initial_data=None):
        # initial_data: Liste von Dicts (so wie aus Supabase)
        self.data = initial_data or []

    class _Query:
        def __init__(self, table, filters=None):
            self._table = table
            self._filters = filters or []

        def eq(self, field, value):
            self._filters.append((field, value))
            return self

        def _apply_filters(self, rows):
            result = rows
            for field, value in self._filters:
                result = [r for r in result if r.get(field) == value]
            return result

        def select(self, *args, **kwargs):
            # Dummy, nur für Kompatibilität
            return self

        def execute(self):
            rows = self._apply_filters(self._table.data)
            return type("Resp", (), {"data": rows})

        def update(self, values: dict):
            # Update wird direkt ausgeführt und Query-Objekt zurückgegeben
            rows = self._apply_filters(self._table.data)
            for row in rows:
                row.update(values)
            return self

    def select(self, *args, **kwargs):
        return MockDBTable._Query(self)

    def update(self, values: dict):
        return MockDBTable._Query(self).update(values)


class MockSupabaseClient:
    def __init__(self):
        # Beispiel-Daten wie in deiner echten snacks-Tabelle
        self._tables = {
            "snacks": MockDBTable(initial_data=[
                {
                    "id": 1,
                    "name": "Schoko",
                    "price": 1.20,
                    "quantity": 10,
                    "image_url": "chocolate.png",
                    "active": True,
                },
                {
                    "id": 2,
                    "name": "Chips",
                    "price": 1.00,
                    "quantity": 8,
                    "image_url": "chips.png",
                    "active": True,
                },
                {
                    "id": 3,
                    "name": "Gummibärchen",
                    "price": 0.80,
                    "quantity": 15,
                    "image_url": "gummy.png",
                    "active": True,
                },
                # ... bis zu 9 Produkte
            ])
        }

    def table(self, name: str):
        return self._tables[name]
