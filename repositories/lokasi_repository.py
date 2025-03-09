from entity.lokasi import Lokasi
from database import db

class LokasiRepository:
    
    @staticmethod
    def get_all_lokasi():
        return Lokasi.query.filter_by(is_deleted=False).all()
    
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
    
    