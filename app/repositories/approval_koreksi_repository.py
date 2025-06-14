from app.database import db
from app.entity import ApprovalKoreksi
from datetime import date
from sqlalchemy.orm import joinedload
from dateutil.relativedelta import relativedelta

from app.utils.app_constans import AppConstants


class ApprovalKoreksiRepository:

    @staticmethod
    def get_list_pagination(user_id, filter_status, page = 1, size = 10):

        today = date.today()
        three_months_ago = today - relativedelta(months=3)

        query = ApprovalKoreksi.query.filter(
            ApprovalKoreksi.user_id == user_id,
            ApprovalKoreksi.created_date >= three_months_ago
        )

        if filter_status != AppConstants.APPROVAL_STATUS_ALL.value:
            query = query.filter(
                ApprovalKoreksi.status == filter_status,
            )

        query = query.order_by(ApprovalKoreksi.created_date.desc())

        return query.paginate(page=page, per_page=size, error_out=False)

    @staticmethod
    def get_detail_by_id(user_id, approval_id):
        query = ApprovalKoreksi.query.options(joinedload(ApprovalKoreksi.detail_approval)).filter_by(id=approval_id,
                                                                                             user_id=user_id)
        return query.first()

    @staticmethod
    def create_approval_koreksi_user(data):
        new_koreksi = ApprovalKoreksi(
            absensi_date=data['absensi_date'],
            status=data['status'],
            approval_user_id=data['approval_user_id'],
            absensi_id=data['absensi_id'],
            user_id=data['user_id']
        )

        db.session.add(new_koreksi)
        db.session.flush()

        return new_koreksi

    @staticmethod
    def delete_koreksi(approval):
        parent_absensi = approval.absensi

        for detail_approval in approval.detail_approval:
            db.session.delete(detail_approval)

        db.session.delete(approval)

        if parent_absensi and parent_absensi.metode == AppConstants.KOREKSI_KEHADIRAN.value:
            db.session.delete(parent_absensi)