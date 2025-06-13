from app.database import db
from app.entity.libur import Libur
from sqlalchemy import or_, cast

class LiburRepository:

    @staticmethod
    def get_libur_pagination(page: int = 1, size: int = 10, search: str = None):

        query = db.session.query(
            Libur.id,
            Libur.date,
            Libur.is_holiday,
            Libur.description
        )

        if search:
            query = query.filter(
                or_(
                    Libur.description.ilike(f"%{search}%"),
                    cast(Libur.date, db.String).ilike(f"%{search}%")
                )
            )

        query = query.order_by(Libur.date.asc())

        pagination = query.paginate(page=page, per_page=size, error_out=False)

        return pagination

    @staticmethod
    def get_libur_by_id(libur_id):
        return Libur.query.filter_by(id=libur_id).first()

    @staticmethod
    def update_libur(libur : Libur, data):
        libur.date = data['date']
        libur.is_holiday = data['is_holiday']
        libur.description = data['description']
        db.session.commit()

        return libur

    @staticmethod
    def delete_libur(libur : Libur):
        db.session.delete(libur)
        db.session.commit()

    @staticmethod
    def create_libur(data):
        new_libur = Libur(date=data['date'], is_holiday=data['is_holiday'], description=data['description'])

        db.session.add(new_libur)
        db.session.commit()

        return new_libur