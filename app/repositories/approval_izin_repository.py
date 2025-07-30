from app.database import db
from app.entity import ApprovalIzin
from datetime import date
from sqlalchemy.orm import joinedload
from dateutil.relativedelta import relativedelta
from app.utils.app_constans import AppConstants
from datetime import date, datetime
from sqlalchemy import extract


class ApprovalIzinRepository:
    @staticmethod
    def create_approval_izin(data):
        new_approval = ApprovalIzin(
            status = data['status'],
            approval_user_id = data['approval_user_id'],
            izin_id = data['izin_id'],
            user_id = data['user_id'],
        )
        db.session.add(new_approval)
        db.session.flush()
        return new_approval

    @staticmethod
    def get_list_pagination(user_id, search, filter_status, page=1, size=10):
        query = ApprovalIzin.query.filter(
            ApprovalIzin.user_id == user_id
        )

        if search:
            search_date = datetime.strptime(search, '%Y-%m')

            query = query.filter(
                extract('year', ApprovalIzin.created_date) == search_date.year,
                extract('month', ApprovalIzin.created_date) == search_date.month
            )

        if filter_status != AppConstants.APPROVAL_STATUS_ALL.value:
            query = query.filter(
                ApprovalIzin.status == filter_status,
            )

        query = query.order_by(ApprovalIzin.created_date.desc())

        return query.paginate(page=page, per_page=size, error_out=False)

    @staticmethod
    def get_list_pagination_approval_user(user_id, page=1, size=10, filter_month=None, filter_status=None):
        query = ApprovalIzin.query.filter(
            ApprovalIzin.approval_user_id == user_id
        )

        if filter_month:
            search_date = datetime.strptime(filter_month, '%Y-%m')

            query = query.filter(
                extract('year', ApprovalIzin.created_date) == search_date.year,
                extract('month', ApprovalIzin.created_date) == search_date.month
            )

        if filter_status and filter_status != AppConstants.APPROVAL_STATUS_ALL.value:
            query = query.filter(
                ApprovalIzin.status == filter_status
            )

        query = query.order_by(ApprovalIzin.created_date.desc())

        return query.paginate(page=page, per_page=size, error_out=False)

    @staticmethod
    def get_detail_by_id(user_id, approval_id):
        query = ApprovalIzin.query.options(joinedload(ApprovalIzin.izin)).filter_by(id=approval_id, user_id=user_id)
        return query.first()

    @staticmethod
    def delete_approval_izin(approval):
        izin = approval.izin

        db.session.delete(izin)

        db.session.delete(approval)

    @staticmethod
    def get_detail_by_id_and_approval_user_id(approval_id, approval_user_id):
        query = ApprovalIzin.query.options(joinedload(ApprovalIzin.izin)).filter_by(id=approval_id, approval_user_id=approval_user_id)
        return query.first()
