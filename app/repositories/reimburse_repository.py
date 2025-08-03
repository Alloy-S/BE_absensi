from app.database import db
from app.entity import ApprovalKoreksi, Reimburse, Users, DataKaryawan
from datetime import date
from sqlalchemy.orm import joinedload
from dateutil.relativedelta import relativedelta
from datetime import datetime
from sqlalchemy import extract, or_
from app.utils.app_constans import AppConstants


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

    @staticmethod
    def get_history_reimburse_admin(page: int = 1, per_page: int = 10, filter_month=None, search=None):
        query = db.session.query(
            Reimburse
        )

        if filter_month:
            search_date = datetime.strptime(filter_month, '%Y-%m')

            query = query.filter(
                extract('year', Reimburse.date) == search_date.year,
                extract('month', Reimburse.date) == search_date.month
            )

        if search:
            search_string = f"%{search}%"

            query = query.join(Users, Reimburse.created_by == Users.id).join(DataKaryawan, Users.id == DataKaryawan.user_id)

            query = query.filter(
                or_(
                    Users.fullname.ilike(search_string),
                    DataKaryawan.nip.ilike(search_string)
                )
            )

        query = query.filter(Reimburse.status == AppConstants.APPROVED.value)

        query = query.order_by(Reimburse.date.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination

    @staticmethod
    def get_reimburse_by_id(reimburse_id):
        return Reimburse.query.filter_by(id=reimburse_id).first()