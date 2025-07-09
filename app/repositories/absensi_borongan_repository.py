from app.database import db
from app.entity import AbsensiBorongan
from app.entity import ApprovalAbsensiBorongan
from sqlalchemy.orm import joinedload

class AbsensiBoronganRepository:
    @staticmethod
    def create(data):
        new_absensi = AbsensiBorongan(
            total=data["total"],
            date=data["date"],
            status=data["status"]
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