from app.utils.app_constans import AppConstants
from app.database import db
from app.entity import Izin, Users, DataKaryawan
from datetime import datetime
from sqlalchemy import extract, or_


class IzinRepository:
    @staticmethod
    def create_izin(data):
        new_izin = Izin(
            tgl_izin_start=data['tgl_izin_start'],
            tgl_izin_end=data['tgl_izin_end'],
            keterangan=data['keterangan'],
            status=data['status'],
            jenis_izin_id=data['jenis_izin_id'],
            user_id=data['user_id'],
        )
        db.session.add(new_izin)
        db.session.flush()
        return new_izin

    @staticmethod
    def get_izin_by_date(user_id, izin_date):
        return Izin.query.filter(
            Izin.user_id == user_id,
            Izin.tgl_izin_start == izin_date,
            Izin.status.in_([AppConstants.WAITING_FOR_APPROVAL.value, AppConstants.APPROVED.value]),
        ).first()

    @staticmethod
    def get_history_izin_admin(page: int = 1, per_page: int = 10, filter_month=None, search=None):
        query = db.session.query(
            Izin
        )

        if filter_month:
            search_date = datetime.strptime(filter_month, '%Y-%m')

            query = query.filter(
                extract('year', Izin.tgl_izin_start) == search_date.year,
                extract('month', Izin.tgl_izin_start) == search_date.month
            )

        if search:
            search_string = f"%{search}%"

            query = query.join(Users, Izin.user_id == Users.id).join(DataKaryawan, Users.id == DataKaryawan.user_id)

            query = query.filter(
                or_(
                    Users.fullname.ilike(search_string),
                    DataKaryawan.nip.ilike(search_string)
                )
            )

        query = query.filter(Izin.status == AppConstants.APPROVED.value)

        query = query.order_by(Izin.date.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination

    @staticmethod
    def get_izin_by_id(izin_id):
        return Izin.query.filter_by(id=izin_id).first()
