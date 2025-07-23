from app.database import db
from app.entity import ApprovalKoreksi, Reimburse
from datetime import date
from sqlalchemy.orm import joinedload
from dateutil.relativedelta import relativedelta


class ReimburseRepository:

    @staticmethod
    def create_reimburse(data):
        new_reimburse = Reimburse(
            status = data['status'],
            photo_id = data['photo_id'],
            created_by = data['created_by']
        )

        db.session.add(new_reimburse)
        db.session.flush()

        return new_reimburse

    @staticmethod
    def delete_reimburse(reimburse_id):
        reimburse = Reimburse.query.filter_by(id=reimburse_id).first()

        db.session.delete(reimburse)