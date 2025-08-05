from app.entity import DetailJadwalKerja, DataKaryawan
from app.entity.jadwal_kerja import JadwalKerja
from app.database import db
from sqlalchemy import or_

class JadwalKerjaRepository:

    @staticmethod
    def get_all():
        query = db.session.query(
            JadwalKerja.id,
            JadwalKerja.kode,
            JadwalKerja.shift,
        ).order_by(JadwalKerja.shift.asc())

        result = query.all()
        return result

    @staticmethod
    def get_all_pagination(page: int = 1, size: int = 10, search: str = None):

        query = db.session.query(
            JadwalKerja.id,
            JadwalKerja.kode,
            JadwalKerja.shift,
            JadwalKerja.is_active,
        )

        if search:
            query = query.filter(
                or_(
                    JadwalKerja.kode.ilike(f"%{search}%"),
                    JadwalKerja.shift.ilike(f"%{search}%")
                )
            )

        query = query.order_by(JadwalKerja.shift.asc())

        pagination = query.paginate(page=page, per_page=size, error_out=False)

        return pagination

    @staticmethod
    def get_by_id(id) -> JadwalKerja:
        return JadwalKerja.query.join(DetailJadwalKerja, JadwalKerja.id == DetailJadwalKerja.jadwal_kerja_id).filter(
            JadwalKerja.id == id).first()

    @staticmethod
    def get_by_name(shift) -> JadwalKerja:
        return JadwalKerja.query.filter_by(shift=shift).first()

    @staticmethod
    def get_by_kode(kode) -> JadwalKerja:
        return JadwalKerja.query.filter_by(kode=kode).first()

    @staticmethod
    def create_jadwal(kode, shift, details: list) -> JadwalKerja:
        jadwal_kerja = JadwalKerja(kode=kode, shift=shift)
        db.session.add(jadwal_kerja)
        db.session.flush()

        for detail in details:
            detail_jadwal = DetailJadwalKerja(
                hari=detail['hari'],
                time_in=detail['time_in'],
                time_out=detail['time_out'],
                toler_in=detail['toler_in'],
                toler_out=detail['toler_out'],
                jadwal_kerja_id=jadwal_kerja.id,
                is_active=detail.get('is_active', True),
            )
            db.session.add(detail_jadwal)

        db.session.commit()
        return jadwal_kerja

    @staticmethod
    def create_new_version(old_jadwal_kerja: JadwalKerja, kode, shift, details: list, migrate_data=True) -> JadwalKerja:
        JadwalKerjaRepository.non_aktif_jadwal(old_jadwal_kerja)

        new_jadwal_kerja = JadwalKerja(
            kode=kode,
            shift=shift,
            parent_schedule_id=old_jadwal_kerja.id
        )

        db.session.add(new_jadwal_kerja)
        db.session.flush()

        if migrate_data:
            karyawan_to_migrate = DataKaryawan.query.filter_by(
                jadwal_kerja_id=old_jadwal_kerja.id
            ).with_for_update().all()

            for karyawan in karyawan_to_migrate:
                karyawan.jadwal_kerja_id = new_jadwal_kerja.id

        for detail in details:
            detail_jadwal = DetailJadwalKerja(
                hari=detail['hari'],
                time_in=detail['time_in'],
                time_out=detail['time_out'],
                toler_in=detail['toler_in'],
                toler_out=detail['toler_out'],
                jadwal_kerja_id=new_jadwal_kerja.id,
                is_active=detail.get('is_active', True),
            )
            db.session.add(detail_jadwal)

        db.session.commit()
        return new_jadwal_kerja

    @staticmethod
    def non_aktif_jadwal(jadwal_kerja: JadwalKerja):

        jadwal_kerja.is_active = False
        db.session.commit()

    @staticmethod
    def aktif_jadwal(jadwal_kerja: JadwalKerja):

        jadwal_kerja.is_active = True
        db.session.commit()
