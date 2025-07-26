from app.database import db
from app.entity import Izin


class IzinRepository:
    @staticmethod
    def create_izin(data):
        new_izin = Izin(
            tgl_izin_start=data['tgl_izin_start'],
            tgl_izin_end=data['tgl_izin_end'],
            keterangan=data['keterangan'],
            status=data['status'],
            jenis_izin_id=data['jenis_izin_id'],
            user_id=data['user_id'],
        )
        db.session.add(new_izin)
        db.session.flush()
        return new_izin

    @staticmethod
    def get_izin_by_date(user_id, izin_date):
        return Izin.query.filter_by(
            user_id=user_id,
            tgl_izin_start=izin_date
        ).first()
