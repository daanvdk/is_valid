class IsValidMixin:
    def assertIsValid(self, validator, data, msg=None):
        valid, error = validator(data, detailed=True)
        self.assertTrue(valid, msg=str(error) if msg is None else msg)
