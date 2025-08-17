from app.database import db
from app.entity import JenisIzin

class JenisIzinRepository:
    @staticmethod
    def create(data):
        new_jenis_izin = JenisIzin(
            nama=data['nama'],
            kuota_default=data.get('kuota_default', 0),
            periode_reset=data.get('periode_reset', 'TIDAK_ADA'),
            berlaku_setelah_bulan=data.get('berlaku_setelah_bulan', 0),
            is_paid=data.get('is_paid', False),
        )
        db.session.add(new_jenis_izin)
        db.session.commit()
        return new_jenis_izin

    @staticmethod
    def get_all():
        return JenisIzin.query.order_by(JenisIzin.nama).all()

    @staticmethod
    def get_list_pagination(page, size, search):
        query = JenisIzin.query

        if search:
            query = query.filter(JenisIzin.nama.ilike(f"%{search}%"))

        query = query.order_by(JenisIzin.nama.asc())

        return query.paginate(page=page, per_page=size, error_out=False)

    @staticmethod
    def get_by_id(jenis_izin_id):
        return JenisIzin.query.get(jenis_izin_id)

    @staticmethod
    def find_by_name(name):
        return JenisIzin.query.filter_by(nama=name).first()

    @staticmethod
    def update(jenis_izin_obj, data):
        jenis_izin_obj.nama = data['nama']
        jenis_izin_obj.kuota_default = data['kuota_default']
        jenis_izin_obj.periode_reset = data['periode_reset']
        jenis_izin_obj.berlaku_setelah_bulan = data['berlaku_setelah_bulan']
        jenis_izin_obj.is_paid = data['is_paid']
        db.session.commit()
        return jenis_izin_obj

    @staticmethod
    def delete(jenis_izin_obj):
        db.session.delete(jenis_izin_obj)
        db.session.commit()

    @staticmethod
    def find_by_reset_period(period: str):
        return JenisIzin.query.filter_by(periode_reset=period).all()