from entity.jadwal_kerja import JadwalKerja
from database import db

class JadwalKerjaRepository:
    
    @staticmethod
    def get_all():
        return JadwalKerja.query.all()

    @staticmethod
    def get_all_pagination(page: int = 1, per_page: int = 10, search: str = None):
        print(f"Fetching all Jabatan with pagination: page={page}, per_page={per_page}, search={search}")
    
    @staticmethod
    def get_by_id(id) -> JadwalKerja:
        return JadwalKerja.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_name(shift) -> JadwalKerja:
        return JadwalKerja.query.filter_by(shift=shift).first()
    
    @staticmethod
    def create(shift, timeIn, timeOut, tolerIn, tolerOut) -> JadwalKerja:
        jadwalKerja = JadwalKerja(shift=shift, time_in=timeIn, time_out=timeOut, toler_in=tolerIn, toler_out=tolerOut)
        db.session.add(jadwalKerja)
        db.session.commit()
        return jadwalKerja
    
    @staticmethod
    def update(jadwalKerja:JadwalKerja, shift, timeIn, timeOut, tolerIn, tolerOut) -> JadwalKerja:
        jadwalKerja.shift = shift
        jadwalKerja.time_in = timeIn
        jadwalKerja.time_out = timeOut
        jadwalKerja.toler_in = tolerIn
        jadwalKerja.toler_out = tolerOut
        db.session.commit()
        return jadwalKerja
    
    @staticmethod
    def delete(jadwalKerja:JadwalKerja):
        db.session.delete(jadwalKerja)
    
    