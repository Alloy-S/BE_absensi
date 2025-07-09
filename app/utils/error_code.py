from enum import Enum

class ErrorCode(Enum):

    RESOURCE_NOT_FOUND = ("{resource} not found", 404)
    ALREADY_INACTIVE = ("{resource} sudah tidak aktif", 400)
    INCORRECT_PASSWORD_OR_USERNAME = ("Username atau Password salah", 400)
    SEND_NOTIFICATION_FAILED = ("GAGAL_MENGIRIM_NOTIFIKASI", 400)
    USER_LOCATION_NOT_MATCH_REQUIREMENT = ("Anda berada di luar jangkauan lokasi kerja yang diizinkan.", 400)
    USER_FACE_NOT_MATCH_REQUIREMENT = ("Verifikasi wajah gagal. Pastikan wajah terlihat jelas dan sesuai.", 400)
    TODAY_IS_HOLIDAY = ("Hari Ini Merupakan Hari Libur. Tidak Perlu Melakukan Presensi", 400)
    ATTENDANCE_TYPE_NOT_VALID = ("Jenis Presensi Tidak Ada", 400)
    INVALID_DATE_FORMAT = ("Format waktu salah.", 400)
    CANCELLATION_NOT_ALLOWED = ("Tidak Dapat Melakukan Pembatalan Pengajuan", 400)
    APPROVER_NOT_FOUND = ("PIC Karyawan Tidak Ditemukan. Hubungi Admin untuk lebih lanjut", 400)

    @property
    def message(self):
        return self.value[0]

    @property
    def status_code(self):
        return self.value[1]