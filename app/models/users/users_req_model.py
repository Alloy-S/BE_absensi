from marshmallow import Schema, fields, validate, ValidationError, EXCLUDE


class DataPribadiSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    gender = fields.String(required=True)
    tmpt_lahir = fields.String(required=True)
    tgl_lahir = fields.Date(required=True)
    status_kawin = fields.String(required=False)
    agama = fields.String(required=False)
    gol_darah = fields.String(required=False)

class DataKontakSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    no_telepon = fields.String(required=True)
    alamat = fields.String(required=True)
    nama_darurat = fields.String(required=True)
    no_telepon_darurat = fields.String(required=True)
    relasi_darurat = fields.String(required=True)

class DataKaryawanSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    tgl_gabung = fields.String(required=True)
    gaji_pokok = fields.Float(required=False, allow_none=True)
    face_recognition_mode = fields.String(required=True)
    lokasi_id = fields.String(required=True)
    jabatan_id = fields.String(required=True)
    jadwal_kerja_id = fields.String(required=True)
    tipe_karyawan = fields.String(required=True)
    user_pic_id = fields.String(required=False, allow_none=True)
    grup_gaji_id = fields.String(required=False, allow_none=True)

class UserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    fullname = fields.String(required=True)
    data_pribadi = fields.Nested(DataPribadiSchema, required=True)
    data_kontak = fields.Nested(DataKontakSchema, required=True)
    data_karyawan = fields.Nested(DataKaryawanSchema, required=True)

class ResendLoginSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user_id = fields.String(required=True)

class ResetPasswordSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    old_pass = fields.String(required=True)
    new_pass = fields.String(required=True)
    verify_pass = fields.String(required=True)

class FCMToken(Schema):
    class Meta:
        unknown = EXCLUDE

    fcm_token = fields.String(required=True)

