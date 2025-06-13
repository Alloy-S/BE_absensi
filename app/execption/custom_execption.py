from app.utils.error_code import ErrorCode


class GeneralException(Exception):
    def __init__(self, error_code):
        if not isinstance(error_code, ErrorCode):
            raise TypeError("error_code harus merupakan instance dari ErrorCode")

        self.message = error_code.message
        self.status_code = error_code.status_code

        super().__init__(self.message)


class GeneralExceptionWithParam(Exception):
    def __init__(self, error_code, params):
        if not isinstance(error_code, ErrorCode):
            raise TypeError("error_code harus merupakan instance dari ErrorCode")

        self.error_code_member = error_code
        self.params = params or {}

        # Format pesan dari template di Enum
        self.message = self.error_code_member.message.format(**self.params)
        self.status_code = self.error_code_member.status_code

        super().__init__(self.message)