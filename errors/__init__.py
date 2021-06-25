class SimpleError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code