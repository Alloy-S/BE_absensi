from app.entity import DetailJadwalKerja
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
        print(f"Fetching all Jabatan with pagination: page={page}, per_page={size}, search={search}")

        query = db.session.query(
            JadwalKerja.id,
            JadwalKerja.kode,
            JadwalKerja.shift

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
    def create(kode, shift, isSameHour, details: list) -> JadwalKerja:
        jadwalKerja = JadwalKerja(kode=kode, shift=shift, is_same_hour=isSameHour)
        db.session.add(jadwalKerja)
        db.session.flush()

        for detail in details:
            detail_jadwal = DetailJadwalKerja(
                hari=detail['hari'],
                time_in=detail['time_in'],
                time_out=detail['time_out'],
                toler_in=detail['toler_in'],
                toler_out=detail['toler_out'],
                jadwal_kerja_id=jadwalKerja.id
            )
            db.session.add(detail_jadwal)

        db.session.commit()
        return jadwalKerja

    @staticmethod
    def update(jadwalKerja: JadwalKerja, kode, shift, isSameHour, details: list) -> JadwalKerja:
        jadwalKerja.kode = kode
        jadwalKerja.shift = shift
        JadwalKerja.is_same_hour = isSameHour

        DetailJadwalKerja.query.filter_by(jadwal_kerja_id=jadwalKerja.id).delete()

        for detail in details:
            new_detail = DetailJadwalKerja(
                hari=detail['hari'],
                time_in=detail['time_in'],
                time_out=detail['time_out'],
                toler_in=detail['toler_in'],
                toler_out=detail['toler_out'],
                jadwal_kerja_id=jadwalKerja.id
            )
            db.session.add(new_detail)

        db.session.commit()
        return jadwalKerja

    @staticmethod
    def delete(jadwalKerja: JadwalKerja):

        DetailJadwalKerja.query.filter_by(jadwal_kerja_id=jadwalKerja.id).delete()

        JadwalKerja.query.filter_by(id=jadwalKerja.id).delete()

        db.session.commit()
