from app.database import db
from app.entity import KomponenGaji
from sqlalchemy import or_


class KomponenGajiRepository:

    @staticmethod
    def create_kom_gaji(data):
        new_kom_gaji = KomponenGaji(
            kom_kode=data['kom_kode'],
            kom_name=data['kom_name'],
            no_urut=data['no_urut'],
            tipe=data['tipe'],
            hitung=data['hitung'],
        )

        db.session.add(new_kom_gaji)
        db.session.commit()

        return new_kom_gaji

    @staticmethod
    def get_kom_gaji_by_id(kom_gaji_id):
        return KomponenGaji.query.filter_by(id=kom_gaji_id).first()

    @staticmethod
    def get_kom_gaji_by_kode(kom_gaji_kode):
        return KomponenGaji.query.filter_by(kom_kode=kom_gaji_kode).first()

    @staticmethod
    def update_kom_gaji(kom_gaji, data):
        kom_gaji.kom_kode = data['kom_kode']
        kom_gaji.kom_name = data['kom_name']
        kom_gaji.no_urut = data['no_urut']
        kom_gaji.tipe = data['tipe']
        kom_gaji.hitung = data['hitung']

        db.session.commit()

        return kom_gaji

    @staticmethod
    def get_kom_gaji_pagination(search, page=1, size=10):
        query = KomponenGaji.query

        if search:
            query = query.filter(
                or_(
                    KomponenGaji.kom_kode.ilike(f"%{search}%"),
                    KomponenGaji.kom_name.ilike(f"%{search}%"),
                )
            )

        query = query.order_by(KomponenGaji.kom_kode.asc())

        return query.paginate(page=page, per_page=size, error_out=False)

    @staticmethod
    def delete_kom_gaji(kom_gaji):
        db.session.delete(kom_gaji)
        db.session.commit()

    @staticmethod
    def get_all_kom_gaji():
        return KomponenGaji.query.all()
