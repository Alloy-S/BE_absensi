from app.database import db
from app.entity import Perusahaan
from datetime import datetime

class PerusahaanRepository:

    @staticmethod
    def get_profile_perusahaan():
        return Perusahaan.query.first()

    @staticmethod
    def edit_profile_perusahaan(perusahaan, data, user_id):
        perusahaan.alamat = data.get('alamat', perusahaan.alamat)
        perusahaan.kota_kabupaten = data.get('kota_kabupaten', perusahaan.kota_kabupaten)
        perusahaan.provinsi = data.get('provinsi', perusahaan.provinsi)
        perusahaan.negara = data.get('negara', perusahaan.negara)
        perusahaan.no_telepon = data.get('no_telepon', perusahaan.no_telepon)
        perusahaan.kode_pos = data.get('kode_pos', perusahaan.kode_pos)
        perusahaan.nama = data.get('nama', perusahaan.nama)
        perusahaan.updated_by = user_id
        perusahaan.date_updated = datetime.now()

        db.session.commit()

        return perusahaan