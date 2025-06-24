from app.database import db
from app.entity import JenisIzin

class JenisIzinRepository:

    @staticmethod
    def get_all_jenis_izin():
        return JenisIzin.query.all()