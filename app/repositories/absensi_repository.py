from app.database import db
from app.entity import Absensi

class AbsensiRepository:

    @staticmethod
    def get_absensi_by_id(absensi_id):
        return Absensi.query.filter_by(id=absensi_id).first()
