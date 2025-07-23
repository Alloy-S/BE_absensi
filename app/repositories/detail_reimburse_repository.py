from app.database import db
from app.entity import DetailReimburse
from datetime import date
from sqlalchemy.orm import joinedload
from dateutil.relativedelta import relativedelta


class DetailReimburseRepository:

    @staticmethod
    def create_detail_reimburse(data):
        new_detail_reimburse = DetailReimburse(
            nama=data['nama'],
            harga=data['harga'],
            jumlah=data['jumlah'],
            reimburse_id=data['reimburse_id']
        )

        db.session.add(new_detail_reimburse)
        db.session.flush()
        return new_detail_reimburse

    @staticmethod
    def delete_detail_reimburse(reimburse_id):

        details_to_delete = DetailReimburse.query.filter_by(reimburse_id=reimburse_id).all()

        for detail in details_to_delete:
            db.session.delete(detail)

        return len(details_to_delete)
