class ActionValidationError(Exception):
    errors = None

    def __init__(self, errors, *args):
        self.errors = errors
        super().__init__(errors, *args)
