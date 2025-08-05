from app.utils.app_constans import AppConstants
from app.database import db
from app.entity import JatahKuotaCuti, Libur
from sqlalchemy.orm import joinedload
from datetime import timedelta
from app.repositories.user_repository import UserRepository


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

    @staticmethod
    def calculate_effective_duration(user, start_date, end_date):

        if not user.data_karyawan.jadwal_kerja:
            return (end_date - start_date).days + 1

        detail_jadwal_kerja = user.data_karyawan.jadwal_kerja.detail_jadwal_kerja
        libur = Libur.query.filter(Libur.date.between(start_date, end_date)).all()

        hari_libur = {h.date for h in libur}

        efektif_hari_kerja = {detail.hari.value for detail in detail_jadwal_kerja if detail.is_active}

        effective_days = 0
        current_date = start_date

        while current_date <= end_date:
            if current_date not in hari_libur:
                day_of_haliday = current_date.weekday()
                day_name = AppConstants.DAY_MAP.value.get(day_of_haliday)

                if day_name in efektif_hari_kerja:
                    effective_days += 1

            current_date += timedelta(days=1)

        return effective_days