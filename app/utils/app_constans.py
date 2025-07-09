from enum import Enum

class AppConstants(Enum):
    ADMIN_ROLE = "admin"
    HRD_ROLE = "HRD"
    KARYAWAN_ROLE = "Karyawan"

    ADMIN_GROUP = (ADMIN_ROLE, HRD_ROLE)
    USER_GROUP = (KARYAWAN_ROLE, ADMIN_ROLE, HRD_ROLE)

    USER_RESOURCE = "User"
    ABSENSI_RESOURCE = "Absensi"
    ABSENSI_BORONGAN_RESOURCE = "Absensi Borongan"
    APPROVAL_KOREKSI_RESOURCE = "Approval Koreksi"
    APPROVAL_ABSENSI_BORONGAN_RESOURCE = "Approval Absensi borongan"
    IZIN_RESOURCE = "Izin"
    LEMBUR_RESOURCE = "Lembur"
    HARGA_RESOURCE = "Harga Harian Borongan"

    LOCATION = "Lokasi Absen"

    ATTENDANCE_IN = "IN"
    ATTENDANCE_OUT = "OUT"

    ON_TIME = "Hadir"
    LATE = "Datang Terlambat"
    EARLY = "Pulang Terlalu Cepat"

    APPROVED = "Disetujui"
    WAITING_FOR_APPROVAL = "Menunggu Persetujuan"
    REJECTED = "Ditolak"
    APPROVAL_STATUS_ALL = "All"

    HOLIDAY = "Libur"
    WORK = "Masuk"

    FACE_RECOGNITION = "Face Recognition"
    KOREKSI_KEHADIRAN = "Koreksi Kehadiran"

    UPLOAD_FOLDER = 'temp_uploads'

    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

