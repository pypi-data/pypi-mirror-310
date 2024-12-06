class VisionDecodeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InputTokensError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InputNullTokensError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
