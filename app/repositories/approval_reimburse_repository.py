from app.database import db
from app.entity import ApprovalReimburse
from app.entity import Reimburse
from datetime import date
from sqlalchemy.orm import joinedload
from app.utils.app_constans import AppConstants
from dateutil.relativedelta import relativedelta
from sqlalchemy import extract
from datetime import date, datetime


class ApprovalReimburseRepository:

    @staticmethod
    def create_approval_reimburse(data, user_id):
        new_approval = ApprovalReimburse(
            status=data['status'],
            approval_user_id=data['approval_user_id'],
            reimburse_id=data['reimburse_id'],
            user_id=user_id
        )

        db.session.add(new_approval)
        db.session.flush()
        return new_approval

    @staticmethod
    def get_approval_pagination(user_id, filter_month, filter_status, page=1, size=10):
        query = ApprovalReimburse.query.filter(
            ApprovalReimburse.user_id == user_id
        )

        if filter_month:
            search_date = datetime.strptime(filter_month, '%Y-%m')

            query = query.filter(
                extract('year', ApprovalReimburse.created_date) == search_date.year,
                extract('month', ApprovalReimburse.created_date) == search_date.month
            )

        if filter_status != AppConstants.APPROVAL_STATUS_ALL.value:
            query = query.filter(
                ApprovalReimburse.status == filter_status,
            )

        query = query.order_by(ApprovalReimburse.created_date.desc())

        return query.paginate(page=page, per_page=size, error_out=False)

    @staticmethod
    def get_approval_by_id(approval_id, user_id):
        query = ApprovalReimburse.query.options(
            joinedload(ApprovalReimburse.reimburse)
        ).filter_by(id=approval_id, user_id=user_id)
        return query.first()

    @staticmethod
    def delete_approval_reimburse(approval_id):
        approval = ApprovalReimburse.query.filter_by(id=approval_id).first()
        db.session.delete(approval)

    @staticmethod
    def get_detail_by_id_and_approval_user_id(approval_id, approval_user_id):
        query = ApprovalReimburse.query.options(
            joinedload(ApprovalReimburse.reimburse),
            joinedload(ApprovalReimburse.approval_user)
        ).filter_by(id=approval_id, approval_user_id=approval_user_id)
        return query.first()

    @staticmethod
    def get_list_pagination_approval_user(pic_id, page=1, size=10, filter_month=None, filter_status=None):
        query = ApprovalReimburse.query.filter(
            ApprovalReimburse.approval_user_id == pic_id
        )

        if filter_month:
            search_date = datetime.strptime(filter_month, '%Y-%m')

            query = query.filter(
                extract('year', ApprovalReimburse.created_date) == search_date.year,
                extract('month', ApprovalReimburse.created_date) == search_date.month
            )

        if filter_status and filter_status != AppConstants.APPROVAL_STATUS_ALL.value:
            query = query.filter(
                ApprovalReimburse.status == filter_status
            )

        query = query.order_by(ApprovalReimburse.created_date.desc())

        return query.paginate(page=page, per_page=size, error_out=False)


