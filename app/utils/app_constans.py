from enum import Enum

class AppConstants(Enum):
    ADMIN_ROLE = "admin"
    HRD_ROLE = "HRD"
    KARYAWAN_ROLE = "Karyawan"

    ADMIN_GROUP = (ADMIN_ROLE, HRD_ROLE)
    USER_GROUP = (KARYAWAN_ROLE, ADMIN_ROLE, HRD_ROLE)

    USER_RESOURCE = "User"
    ABSENSI_RESOURCE = "Absensi"

    LOCATION = "Lokasi Absen"

    ATTENDANCE_IN = "IN"
    ATTENDANCE_OUT = "OUT"

    ON_TIME = "Hadir"
    LATE = "Datang Terlambat"
    EARLY = "Pulang Terlalu Cepat"

    APPROVED = "Disetujui"

    FACE_RECOGNITION = "Face Recognition"

    UPLOAD_FOLDER = 'temp_uploads'

    DATE_FORMAT = "%Y-%m-%d"