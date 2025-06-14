from app.database import db
from app.entity import Absensi

class AbsensiRepository:

    @staticmethod
    def get_absensi_by_id(absensi_id):
        return Absensi.query.filter_by(id=absensi_id).first()

    @staticmethod
    def get_absensi_by_user_id_and_date(user_id, date):
        return Absensi.query.filter_by(user_id=user_id, date=date).first()

    @staticmethod
    def create_absensi(data):
        new_absensi = Absensi(
            date = data['date'],
            lokasi = data['lokasi'],
            metode = data['metode'],
            status = data['status'],
            user_id = data['user_id'],
        )

        db.session.add(new_absensi)
        db.session.flush()

        return new_absensi

