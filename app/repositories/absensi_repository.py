from app.database import db
from app.entity import Absensi, DetailAbsensi, Users, DataKaryawan
from datetime import datetime
from sqlalchemy import extract, or_
from sqlalchemy.orm import joinedload

from app.utils.app_constans import AppConstants


class AbsensiRepository:

    @staticmethod
    def get_absensi_by_id(absensi_id):
        return Absensi.query.filter_by(id=absensi_id).first()

    @staticmethod
    def get_absensi_by_user_id_and_date(user_id, date):
        return Absensi.query.filter_by(user_id=user_id, date=date).first()

    @staticmethod
    def create_absensi(data):
        new_absensi = Absensi(
            date=data['date'],
            lokasi=data['lokasi'],
            metode=data['metode'],
            status=data['status'],
            user_id=data['user_id'],
        )

        db.session.add(new_absensi)
        db.session.flush()

        return new_absensi

    @staticmethod
    def get_absensi_history_by_month_year(user_id, page: int = 1, per_page: int = 10, search = None):
        query = db.session.query(
            Absensi.id,
            Absensi.date,
            Absensi.lokasi,
            Absensi.metode,
            Absensi.status,
            Absensi.user_id
        ).filter(Absensi.user_id == user_id)

        if search:
            search_date = datetime.strptime(search, '%Y-%m')

        else:
            search_date = datetime.today()

        query = query.filter(
            extract('year', Absensi.date) == search_date.year,
            extract('month', Absensi.date) == search_date.month
        )

        query = query.order_by(Absensi.date.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination

    @staticmethod
    def get_history_absensi_admin(page: int = 1, per_page: int = 10, filter_month=None, search=None):
        query = db.session.query(
            Absensi
        )

        if filter_month:
            search_date = datetime.strptime(filter_month, '%Y-%m')

            query = query.filter(
                extract('year', Absensi.date) == search_date.year,
                extract('month', Absensi.date) == search_date.month
            )

        if search:
            search_string = f"%{search}%"

            query = query.join(Users, Absensi.user_id == Users.id).join(DataKaryawan, Users.id == DataKaryawan.user_id)

            query = query.filter(
                or_(
                    Users.fullname.ilike(search_string),
                    DataKaryawan.nip.ilike(search_string)
                )
            )

        query = query.order_by(Absensi.date.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination

    @staticmethod
    def get_absensi_history_detail_by_absensi_id(user_id, absensi_id):
        query = Absensi.query.options(joinedload(Absensi.detail_absensi)).filter(
            Absensi.user_id == user_id,
            Absensi.id == absensi_id,
            Absensi.detail_absensi.any(DetailAbsensi.status_appv == AppConstants.APPROVED.value)
        )

        return query.first()

    @staticmethod
    def get_absensi_history_detail_by_date(user_id, date):
        query = Absensi.query.options(joinedload(Absensi.detail_absensi)).filter(
            Absensi.user_id == user_id,
            Absensi.date == date,
            Absensi.detail_absensi.any(DetailAbsensi.status_appv == AppConstants.APPROVED.value)
        )

        return query.first()