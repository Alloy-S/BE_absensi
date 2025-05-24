from marshmallow import Schema, fields, validate, ValidationError

class DataPribadiSchema(Schema):
    gender = fields.String(required=True)
    tmpt_lahir = fields.String(required=True)
    tgl_lahir = fields.Date(required=True)
    status_kawin = fields.String(required=False)
    agama = fields.String(required=False)
    gol_darah = fields.String(required=False)

class DataKontakSchema(Schema):
    no_telepon = fields.String(required=True)
    alamat = fields.String(required=True)
    provinsi = fields.String(required=False)
    kota = fields.String(required=False)
    nama_darurat = fields.String(required=True)
    no_telepon_darurat = fields.String(required=True)
    relasi_darurat = fields.String(required=True)

class DataKaryawanSchema(Schema):
    # nip = fields.String(required=True)
    tgl_gabung = fields.String(required=True)
    lokasi_id = fields.String(required=True)
    jabatan_id = fields.String(required=True)
    jadwal_kerja_id = fields.String(required=True)
    tipe_karyawan = fields.String(required=True)

class UserSchema(Schema):
    fullname = fields.String(required=True)
    # username = fields.String(required=True)
    # password = fields.String(required=True)
    data_pribadi = fields.Nested(DataPribadiSchema, required=True)
    data_kontak = fields.Nested(DataKontakSchema, required=True)
    data_karyawan = fields.Nested(DataKaryawanSchema, required=True)

