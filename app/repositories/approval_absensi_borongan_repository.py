from app.database import db
from app.entity import ApprovalAbsensiBorongan, AbsensiBorongan


class ApprovalAbsensiBoronganRepository:
    @staticmethod
    def get_list_pagination(user_id, page, size):
        query = ApprovalAbsensiBorongan.query.join(AbsensiBorongan).filter(
            db.or_(
                ApprovalAbsensiBorongan.user_id == user_id
            )
        ).order_by(ApprovalAbsensiBorongan.created_date.desc())
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