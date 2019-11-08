from .is_with import is_with


class is_with_context(is_with):

    def _get_subject(self, data, context):
        return {
            key: values[-1]
            for key, values in context._values.items()
        }
