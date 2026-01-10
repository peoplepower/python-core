# /// script
# requires-python = ">=3.8"
# ///
class CareDailyException(Exception):
    def __init__(self, message, context=None):
        self.message = message
        self.context = context

    def __str__(self):
        return self.message
