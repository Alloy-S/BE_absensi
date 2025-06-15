from app.database import db
from app.entity import ApprovalLembur
from datetime import date
from sqlalchemy.orm import joinedload
from dateutil.relativedelta import relativedelta
from app.utils.app_constans import AppConstants


class ApprovalLemburRepository:
    @staticmethod
    def create_approval_lembur(data):
        new_approval = ApprovalLembur(
            status = data['status'],
            approval_user_id = data['approval_user_id'],
            lembur_id = data['lembur_id'],
            user_id = data['user_id'],
        )
        db.session.add(new_approval)
        db.session.flush()
        return new_approval

    @staticmethod
    def get_list_pagination(user_id, filter_status, page=1, size=10):
        today = date.today()
        three_months_ago = today - relativedelta(months=3)

        query = ApprovalLembur.query.filter(
            ApprovalLembur.user_id == user_id,
            ApprovalLembur.created_date >= three_months_ago
        )

        if filter_status != AppConstants.APPROVAL_STATUS_ALL.value:
            query = query.filter(
                ApprovalLembur.status == filter_status,
            )

        query = query.order_by(ApprovalLembur.created_date.desc())

        return query.paginate(page=page, per_page=size, error_out=False)

    @staticmethod
    def get_detail_by_id(user_id, approval_id):
        query = ApprovalLembur.query.options(joinedload(ApprovalLembur.lembur)).filter_by(id=approval_id, user_id=user_id)
        return query.first()

    @staticmethod
    def delete_approval_lembur(approval):
        lembur = approval.lembur

        db.session.delete(lembur)

        db.session.delete(approval)
