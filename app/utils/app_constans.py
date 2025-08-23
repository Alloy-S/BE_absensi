from enum import Enum


class AppConstants(Enum):
    ADMIN_ROLE = "Admin"
    HRD_ROLE = "HRD"
    KARYAWAN_ROLE = "Karyawan"

    ADMIN_GROUP = (ADMIN_ROLE, HRD_ROLE)
    USER_GROUP = (KARYAWAN_ROLE, ADMIN_ROLE, HRD_ROLE)

    USER_RESOURCE = "User"
    DATA_KONTAK_RESOURCE = "Data Kontak"
    DATA_PRIBADI_RESOURCE = "Data Pribadi"
    DATA_KARYAWAN_RESOURCE = "Data Karyawan"
    ABSENSI_RESOURCE = "Absensi"
    ABSENSI_BY_DATE_RESOURCE = "Tanggal Absensi"
    ABSENSI_BORONGAN_RESOURCE = "Absensi Borongan"
    APPROVAL_KOREKSI_RESOURCE = "Approval Koreksi"
    APPROVAL_ABSENSI_BORONGAN_RESOURCE = "Approval Absensi borongan"
    APPROVAL_REIMBURSE_RESOURCE = "Approval Reimburse"
    APPROVAL_IZIN_RESOURCE = "Approval izin"
    APPROVAL_LEMBUR_RESOURCE = "Approval Lembur"
    PHOTO_RESOURCE = "Photo"
    IZIN_RESOURCE = "Izin"
    LEMBUR_RESOURCE = "Lembur"
    HARGA_RESOURCE = "Harga Harian Borongan"
    PENGUMUMAN_RESOURCE = "Pengumuman"
    REIMBURSE_RESOURCE = "Reimburse"
    JABATAN_RESOURCE = "Jabatan"
    JADWAL_KERJA_RESOURCE = "Jadwal Kerja"
    LOKASI_RESOURCE = "Lokasi Kerja"
    JENIS_IZIN_RESOURCE = "Jenis Izin"
    KUOTA_CUTI_RESOURCE = "Kuota Cuti"
    KOMPONEN_GAJI_RESOURCE = "Komponen Gaji"
    GRUP_GAJI = "Grup Gaji"
    RIWAYAT_PENGGAJIAN_RESOURCE = "Riwayat Penggajian"

    PIC_KARYAWAN = "PIC"

    LOCATION = "Lokasi Absen"

    ATTENDANCE_IN = "IN"
    ATTENDANCE_OUT = "OUT"

    ON_TIME = "Hadir"
    LATE = "Datang Terlambat"
    EARLY = "Pulang Cepat"
    LATE_AND_EARLY = "Datang Terlambat & Pulang Cepat"

    APPROVE_TITLE = "Pengajuan {resource} Disetujui"
    APPROVE_BODY = "Pengajuan {resource} Anda oleh {nama_pengaju} telah disetujui."

    REJECT_TITLE = "Pengajuan {resource} Telah Ditolak"
    REJECT_BODY = "Pengajuan {resource} Telah Ditolak, informasi lebih lanjut dapat menghubungi PIC terkait"

    APPROVED = "Disetujui"
    WAITING_FOR_APPROVAL = "Menunggu Persetujuan"
    REJECTED = "Ditolak"
    APPROVAL_STATUS_ALL = "all"

    REGISTERED = "Terdaftar"
    NOT_REGISTERED = "Tidak Terdaftar"

    HOLIDAY = "Libur"
    WORK = "Masuk"

    FACE_RECOGNITION = "Face Recognition"
    KOREKSI_KEHADIRAN = "Koreksi Kehadiran"

    UPLOAD_FOLDER = 'temp_uploads'

    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    UPLOAD_FOLDER_PHOTO = "uploads/photos"

    GET_LATEST_DATA = 5

    DAY_MAP = {
        0: 'SENIN', 1: 'SELASA', 2: 'RABU', 3: 'KAMIS',
        4: 'JUMAT', 5: 'SABTU', 6: 'MINGGU'
    }
