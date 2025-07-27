from app.database import db
from app.entity import Pengumuman
from datetime import datetime

class PengumumanRepository:

    @staticmethod
    def create_pengumuman(data):
        new_pengumuman = Pengumuman(
            judul=data['judul'],
            isi=data['isi'],
            is_active=True,
            created_by=data['created_by'],
            updated_by=data['created_by']
        )
        db.session.add(new_pengumuman)
        db.session.commit()

        return new_pengumuman

    @staticmethod
    def get_all_pagination_user(page: int = 1, per_page: int = 10, search: str = None):

        query = db.session.query(
            Pengumuman.id,
            Pengumuman.judul,
            Pengumuman.date_created,
        ).filter(Pengumuman.is_active.is_(True))

        if search:
            query = query.filter(Pengumuman.judul.ilike(f"%{search}%"))

        query = query.order_by(Pengumuman.date_created.asc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination

    @staticmethod
    def get_all_pagination_admin(page: int = 1, per_page: int = 10, search: str = None):

        query = db.session.query(
            Pengumuman.id,
            Pengumuman.judul,
            Pengumuman.is_active,
            Pengumuman.date_created,
        )

        if search:
            query = query.filter(Pengumuman.judul.ilike(f"%{search}%"))

        query = query.order_by(Pengumuman.date_created.asc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination

    @staticmethod
    def get_by_id(pengumuman_id):
        return Pengumuman.query.filter_by(id=pengumuman_id).first()

    @staticmethod
    def delete_pengumuman(pengumuman):
        db.session.delete(pengumuman)
        db.session.commit()

    @staticmethod
    def edit_pengumuman(pengumuman, data, user_id):
        pengumuman.judul = data['judul']
        pengumuman.is_active = data['is_active']
        pengumuman.isi = data['isi']
        pengumuman.updated_by = user_id
        pengumuman.date_updated = datetime.now()
        db.session.commit()

        return pengumuman