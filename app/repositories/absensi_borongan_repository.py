from app.database import db
from app.entity import AbsensiBorongan, Users, DataKaryawan
from app.entity import ApprovalAbsensiBorongan
from sqlalchemy.orm import joinedload
from datetime import datetime
from sqlalchemy import extract, or_
from app.utils.app_constans import AppConstants

class AbsensiBoronganRepository:
    @staticmethod
    def create(data):
        new_absensi = AbsensiBorongan(
            total=data["total"],
            date=data["date"],
            status=data["status"],
            created_by=data["created_by"]
        )
        db.session.add(new_absensi)
        db.session.flush()
        return new_absensi

    @staticmethod
    def get_list_pagination(user_id, page, size):
        query = AbsensiBorongan.query.join(ApprovalAbsensiBorongan).filter(
            db.or_(
                ApprovalAbsensiBorongan.user_id == user_id,
                ApprovalAbsensiBorongan.approval_user_id == user_id
            )
        ).order_by(AbsensiBorongan.created_date.desc())
        return query.paginate(page=page, per_page=size, error_out=False)

    @staticmethod
    def get_detail_by_id(absensi_id):
        query = AbsensiBorongan.query.options(
            joinedload(AbsensiBorongan.detail_absensi_borongan)
        ).join(ApprovalAbsensiBorongan).filter(
            AbsensiBorongan.id == absensi_id
        )
        return query.first()

    @staticmethod
    def delete(absensi_obj):
        db.session.delete(absensi_obj)

    @staticmethod
    def get_history_absensi_borongan_admin(page: int = 1, per_page: int = 10, filter_month=None, search=None):
        query = db.session.query(
            AbsensiBorongan
        )

        if filter_month:

            search_date = datetime.strptime(filter_month, '%Y-%m')

            query = query.filter(
                extract('year', AbsensiBorongan.date) == search_date.year,
                extract('month', AbsensiBorongan.date) == search_date.month
            )

        if search:
            search_string = f"%{search}%"

            query = query.join(Users, AbsensiBorongan.created_by == Users.id).join(DataKaryawan, Users.id == DataKaryawan.user_id)

            query = query.filter(
                or_(
                    Users.fullname.ilike(search_string),
                    DataKaryawan.nip.ilike(search_string)
                )
            )

        query = query.filter(AbsensiBorongan.status == AppConstants.APPROVED.value)

        query = query.order_by(AbsensiBorongan.date.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination