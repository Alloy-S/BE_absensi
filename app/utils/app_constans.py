from enum import Enum

class AppConstants(Enum):
    ADMIN_ROLE = "admin"
    HRD_ROLE = "HRD"

    USER_RESOURCE = "User"

    LOCATION = "Lokasi Absen"

    ATTENDANCE_IN = "IN"
    ATTENDANCE_OUT = "OUT"

    ON_TIME = "Hadir"
    LATE = "Datang Terlambat"
    EARLY = "Pulang Terlalu Cepat"

    UPLOAD_FOLDER = 'temp_uploads'