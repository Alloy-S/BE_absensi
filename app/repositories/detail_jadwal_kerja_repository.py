from app.database import db
from app.entity.detail_jadwal_kerja import DetailJadwalKerja

class DetailJadwalKerjaRepository:

    @staticmethod
    def get_detail_jadwal_kerja_by_jadwal_id_and_hari(jadwal_id, hari):

        return DetailJadwalKerja.query.filter_by(jadwal_kerja_id=jadwal_id, hari=hari).first()


