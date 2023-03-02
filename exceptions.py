class IllegalMoveError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class OutOfBoundsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class NotationError(Exception):
    def __init__(self, message: str) -> None:
        # self.value = value
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message
