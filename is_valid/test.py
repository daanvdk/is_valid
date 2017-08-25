class IsValidMixin:
    def assertIsValid(self, predicate, data, msg=None):
        if msg is not None:
            self.assertTrue(predicate(data), msg=msg)
        valid, explanation = predicate(data, explain=True)
        self.assertTrue(valid, msg=str(explanation))
