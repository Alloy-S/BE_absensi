from app.database import db
from app.entity import Lembur, Users, DataKaryawan
from app.utils.app_constans import AppConstants
from datetime import datetime
from sqlalchemy import extract, or_

class LemburRepository:
    @staticmethod
    def create_lembur(data):

        new_lembur = Lembur(
            date_start=data['date_start'],
            date_end=data['date_end'],
            keterangan=data['keterangan'],
            status=data['status'],
            user_id= data['user_id'],
        )
        db.session.add(new_lembur)
        db.session.flush()
        return new_lembur

    @staticmethod
    def get_history_lembur_admin(page: int = 1, per_page: int = 10, filter_month=None, search=None):
        query = db.session.query(
            Lembur
        )

        if filter_month:
            search_date = datetime.strptime(filter_month, '%Y-%m')

            query = query.filter(
                extract('year', Lembur.date_start) == search_date.year,
                extract('month', Lembur.date_start) == search_date.month
            )

        if search:
            search_string = f"%{search}%"

            query = query.join(Users, Lembur.user_id == Users.id).join(DataKaryawan, Users.id == DataKaryawan.user_id)

            query = query.filter(
                or_(
                    Users.fullname.ilike(search_string),
                    DataKaryawan.nip.ilike(search_string)
                )
            )

        query = query.filter(Lembur.status == AppConstants.APPROVED.value)

        query = query.order_by(Lembur.date_start.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination


    @staticmethod
    def get_lembur_by_id(lembur_id):
        return Lembur.query.filter_by(id=lembur_id).first()