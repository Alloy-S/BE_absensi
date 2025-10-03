from enum import Enum

class ErrorCode(Enum):

    KTP_ALREADY_USED = ("Nomor KTP sudah digunakan", 400)
    RESOURCE_NOT_FOUND = ("{resource} tidak ditemukan.", 404)
    RESOURCE_IN_USE = ("{resource} sedang digunakan, tidak bisa melakukan delete.", 400)
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
    NEW_PASSWORD_NOT_MATCH = ("Password Baru Tidak Cocok", 400)
    INCORRECT_PASSWORD = ("Password Lama Tidak Sesuai", 400)
    MANDATORY_PIC = ("Karyawan dengan jabatan ini wajib memiliki PIC/Atasan.", 400)
    HIGHEST_POSITION = ("Jabatan tertinggi tidak boleh memiliki PIC/Atasan.", 400)
    INVALID_BASE64 = ("Format string Base64 tidak valid.", 400)
    INVALID_PHONE_NUMBER_FORMAT = ("Format Nomor Telepon tidak valid. Tidak boleh mengandung huruf", 400)

    FACE_DETECTION_FAILED = ("Gagal Mendeteksi wajah", 400)
    SPOOF_DETECTED = ("Foto terdeteksi palsu. Harap ambil gambar secara langsung.", 400)
    FACE_NOT_FOUND = ("Gagal Mendeteksi wajah, wajah tidak ditemukan.", 400)
    FACE_MORE_THAN_ONE = ("terdeteksi lebih dari 1 wajah, ambil ulang gambar", 400)
    FACE_NOT_REGISTERED = ("Tidak ada wajah terdaftar untuk pengguna ini, Harap Daftarkan wajah terlebih dahulu.", 400)

    DUPLICATE_CORRECTION_REQUEST = ("Sudah ada pengajuan koreksi pada tanggal tersebut", 400)
    DUPLICATE_RESOURCE = ("{resource} sudah terdaftar.", 400)
    DELETION_NOT_ALLOWED = ("Tidak Dapat Melakukan Delete, Item sedang digunakan", 400)
    APPROVER_NOT_ALLOWED = ("Tidak Dapat Melakukan Approval, Item Sudah Di Proses", 400)

    CUTI_INUSE = ("Tidak bisa menghapus jatah cuti yang sudah digunakan.", 400)
    EXISTING_KUOTA_CUTI = ("Karyawan ini sudah memiliki jatah cuti tersebut untuk periode ini.", 400)
    INSUFFICIENT_KUOTA_CUTI = ("Sisa kuota cuti karyawan tidak mencukupi.", 400)

    USER_ROLE_EMPTY = ("Pilih Setidaknya 1 Role.", 400)
    ALREADY_FINAL_STATUS = ("Riwayat sudah difinalisasi.", 400)
    CONN_FAILED_REDIS = ("Koneksi ke Redis gagal. Tidak bisa memulai tugas.", 500)

    FAILED_SYNC_DATA = ("Gagal melakukan sinkronisasi data.", 500)
    EMPTY_GRUP_GAJI = ("Tidak ada karyawan yang terdaftar pada grup gaji ini. Tambahkan setidaknya 1 karyawan.", 400)

    @property
    def message(self):
        return self.value[0]

    @property
    def status_code(self):
        return self.value[1]