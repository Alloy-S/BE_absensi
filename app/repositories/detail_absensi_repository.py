from app.database import db
from app.entity import DetailAbsensi
from app.utils.app_constans import AppConstants


class DetailAbsensiRepository:

    @staticmethod
    def create_detail_absensi(data):
        new_detail_jadwal = DetailAbsensi(
            absensi_id=data['absensi_id'],
            date=data['date'],
            type=data['type'],
            status_appv=data['status_appv'],
            status_absensi=data['status_absensi'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            catatan=data['catatan'],
        )

        db.session.add(new_detail_jadwal)
        db.session.flush()

        return new_detail_jadwal

    @staticmethod
    def delete_detail_absensi_by_absensi_id_and_type(absensi_id, type):
        detail_to_delete = DetailAbsensi.query.filter_by(
            id_absensi=absensi_id,
            type=type
        ).first()

        if detail_to_delete:
            db.session.delete(detail_to_delete)

    @staticmethod
    def delete_detail_absensi_by_absensi_id(absensi_id):
        DetailAbsensi.query.filter_by(
            id_absensi=absensi_id
        ).delete(synchronize_session=False)

    @staticmethod
    def get_detail_by_absensi_id_and_type(absensi_id, type):
        return DetailAbsensi.query.filter_by(
            id_absensi=absensi_id,
            type=type
        ).first()



    @staticmethod
    def get_detail_absensi_by_absensi_id_and_type_and_status_appv(absensi_id, type, status_appv):
        return DetailAbsensi.query.filter_by(absensi_id=absensi_id, type=type, status_appv=status_appv).all()
