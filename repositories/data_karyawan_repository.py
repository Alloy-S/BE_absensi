from entity.data_karyawan import DataKaryawan
from database import db

class DataKaryawanRepository:

    @staticmethod
    def generate_new_nip():
        last_karyawan = db.session.query(DataKaryawan).order_by(DataKaryawan.nip.desc()).first()

        if last_karyawan and last_karyawan.nip.isdigit():
            last_nip = int(last_karyawan.nip)
        else:
            last_nip = 0

        new_nip = str(last_nip + 1).zfill(8)

        return new_nip

    @staticmethod
    def get_latest_nip():
        last_karyawan = db.session.query(DataKaryawan).order_by(DataKaryawan.nip.desc()).first()

        if last_karyawan and last_karyawan.nip.isdigit():
            last_nip = int(last_karyawan.nip)
        else:
            last_nip = 0

        nip = str(last_nip).zfill(8)

        return nip
