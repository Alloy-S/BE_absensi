from app.database import db
from app.entity import ApprovalAbsensiBorongan, AbsensiBorongan
from sqlalchemy import extract
from datetime import date, datetime
from app.utils.app_constans import AppConstants


class ApprovalAbsensiBoronganRepository:
    @staticmethod
    def get_list_pagination(user_id, filter_month, filter_status, page, size):
        query = ApprovalAbsensiBorongan.query.join(AbsensiBorongan).filter(
                ApprovalAbsensiBorongan.user_id == user_id
        ).order_by(ApprovalAbsensiBorongan.created_date.desc())

        if filter_month:
            search_date = datetime.strptime(filter_month, '%Y-%m')

            query = query.filter(
                extract('year', ApprovalAbsensiBorongan.created_date) == search_date.year,
                extract('month', ApprovalAbsensiBorongan.created_date) == search_date.month
            )

        if filter_status != AppConstants.APPROVAL_STATUS_ALL.value:
            query = query.filter(
                ApprovalAbsensiBorongan.status == filter_status,
            )

        query = query.order_by(ApprovalAbsensiBorongan.created_date.desc())

        return query.paginate(page=page, per_page=size, error_out=False)

    @staticmethod
    def create(status, approval_user_id, user_id, absensi_borongan_id):
        new_approval = ApprovalAbsensiBorongan(
            status=status,
            approval_user_id=approval_user_id,
            user_id=user_id,
            absensi_borongan_id=absensi_borongan_id
        )
        db.session.add(new_approval)
        return new_approval

    @staticmethod
    def get_detail_by_id(approval_id):
        return ApprovalAbsensiBorongan.query.filter_by(id=approval_id).first()

    @staticmethod
    def get_detail_by_id_and_user_id(user_id, approval_id):
        return ApprovalAbsensiBorongan.query.filter_by(id=approval_id, user_id=user_id).first()

    @staticmethod
    def delete(approval):
        db.session.delete(approval)