class IsValidMixin:
    """
    A mixin for ``unittest``-like TestCase classes.
    """
    def assertIsValid(self, predicate, data, msg=None):
        """
        Asserts that the data is valid according to the given predicate. If no
        ``msg`` is provided the explanation of the predicate will be used for
        the AssertionError in case the assertion fails.
        """
        if msg is not None:
            self.assertTrue(predicate(data), msg=msg)
        valid, explanation = predicate(data, explain=True)
        self.assertTrue(valid, msg=str(explanation))
