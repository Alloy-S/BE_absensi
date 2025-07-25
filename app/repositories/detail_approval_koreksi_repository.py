from app.database import db
from app.entity import DetailApprovalKoreksi

class DetailApprovalKoreksiRepository:

    @staticmethod
    def create_detaill_approval_koreksi_user(data):
        new_detail_koreksi = DetailApprovalKoreksi(
            approval_koreksi_id=data['approval_koreksi_id'],
            requested_datetime=data['requested_datetime'],
            type=data['type'],
        )

        db.session.add(new_detail_koreksi)
        db.session.flush()

        return new_detail_koreksi