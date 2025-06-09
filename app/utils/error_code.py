from enum import Enum

class ErrorCode(Enum):

    RESOURCE_NOT_FOUND = ("{resource} not found", 404)
    INCORRECT_PASSWORD_OR_USERNAME = ("Username atau Password salah", 400)
    SEND_NOTIFICATION_FAILED = ("GAGAL_MENGIRIM_NOTIFIKASI", 400)

    @property
    def message(self):
        return self.value[0]

    @property
    def status_code(self):
        return self.value[1]