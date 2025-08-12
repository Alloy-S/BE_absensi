from app.database import db
from app.entity import KodePerhitungan


class KodePerhitunganRepository:
    @staticmethod
    def get_all_kode_perhitungan():
        return KodePerhitungan.query.all()