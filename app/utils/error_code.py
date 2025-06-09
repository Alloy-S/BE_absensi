from enum import Enum

class ErrorCode(Enum):

    RESOURCE_NOT_FOUND = ("{resource} not found", 404)

    @property
    def message(self):
        return self.value[0]

    @property
    def status_code(self):
        return self.value[1]