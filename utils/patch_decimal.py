import decimal

def patch_decimal():
    from django.db.backends.sqlite3.operations import DatabaseOperations

    original_get = DatabaseOperations.get_decimalfield_converter

    def safe_get_decimalfield_converter(self, expression):
        original_converter = original_get(self, expression)

        def safe_converter(value, expression, connection):
            try:
                return original_converter(value, expression, connection)
            except decimal.InvalidOperation:
                return decimal.Decimal('0')

        return safe_converter

    DatabaseOperations.get_decimalfield_converter = safe_get_decimalfield_converter

    print("BIENS: Decimal patch applied successfully")