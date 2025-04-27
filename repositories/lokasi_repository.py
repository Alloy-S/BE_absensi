from entity.lokasi import Lokasi
from database import db

class LokasiRepository:
    
    @staticmethod
    def get_all_lokasi():
        return Lokasi.query.filter_by(is_deleted=False).all()

    @staticmethod
    def get_all_pagination(page: int = 1, per_page: int = 10, search: str = None):
        print(f"Fetching all Jabatan with pagination: page={page}, per_page={per_page}, search={search}")

        query = db.session.query(
            Lokasi.id,
            Lokasi.name
        ).filter(Lokasi.is_deleted.is_(False))

        if search:
            query = query.filter(Lokasi.name.ilike(f"%{search}%"))

        query = query.order_by(Lokasi.name.asc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination
    
    @staticmethod
    def get_lokasi_by_id(id) -> Lokasi:
        return Lokasi.query.filter_by(id=id, is_deleted=False).first()
    
    @staticmethod
    def get_lokasi_by_name(name) -> Lokasi:
        return Lokasi.query.filter_by(name=name, is_deleted=False).first()
    
    @staticmethod
    def create_lokasi(name, latitude, longitude, toleransi) -> Lokasi:
        lokasi = Lokasi(name=name, latitude=latitude, longitude=longitude, toleransi=toleransi)
        db.session.add(lokasi)
        db.session.commit()
        return lokasi
    
    @staticmethod
    def update_lokasi(lokasi:Lokasi, name, latitude, longitude, toleransi) -> Lokasi:
        lokasi.name = name
        lokasi.latitude = latitude
        lokasi.longitude = longitude
        lokasi.toleransi = toleransi
        db.session.commit()
        return lokasi
    
    @staticmethod
    def delete_lokasi(lokasi:Lokasi):
        lokasi.is_deleted = True
        db.session.commit()
    
    