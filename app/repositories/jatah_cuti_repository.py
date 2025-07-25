from app.database import db
from app.entity import JatahKuotaCuti
from sqlalchemy.orm import joinedload


class JatahCutiRepository:

    @staticmethod
    def create(user_id, data):
        jatah = JatahKuotaCuti(
            user_id=user_id,
            jenis_izin_id=data['jenis_izin_id'],
            periode=data['periode'],
            kuota_awal=data['kuota_awal'],
            kuota_terpakai=0,
            sisa_kuota=data['kuota_awal']
        )
        db.session.add(jatah)
        db.session.commit()
        return jatah


    @staticmethod
    def get_list_pagination_for_user(user_id, page, size):
        query = JatahKuotaCuti.query.options(
            joinedload(JatahKuotaCuti.jenis_izin)
        ).filter_by(user_id=user_id).order_by(JatahKuotaCuti.periode.desc())

        return query.paginate(page=page, per_page=size, error_out=False)

    @staticmethod
    def get_by_id(jatah_cuti_id):
        return JatahKuotaCuti.query.options(
            joinedload(JatahKuotaCuti.jenis_izin)
        ).get(jatah_cuti_id)

    @staticmethod
    def update(jatah_cuti_obj, data):
        jatah_cuti_obj.kuota_awal = data['kuota_awal']
        jatah_cuti_obj.kuota_terpakai = data['kuota_terpakai']
        jatah_cuti_obj.sisa_kuota = data['kuota_awal'] - data['kuota_terpakai']
        db.session.commit()
        return jatah_cuti_obj

    @staticmethod
    def delete(jatah_cuti_obj):
        db.session.delete(jatah_cuti_obj)
        db.session.commit()

    @staticmethod
    def find_by_user_and_type(user_id, jenis_izin_id, periode):
        return JatahKuotaCuti.query.filter_by(
            user_id=user_id,
            jenis_izin_id=jenis_izin_id,
            periode=periode
        ).first()