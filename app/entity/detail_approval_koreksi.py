from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class DetailApprovalKoreksi(db.Model):
    __tablename__ = 'detail_approval_koreksi'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    approval_koreksi_id = db.Column(UUID(as_uuid=True), db.ForeignKey('approval_koreksi.id'), nullable=False)
    time = db.Column(db.Time, nullable=False)
    type = db.Column(db.String, nullable=False)

    approval = db.relationship("ApprovalKoreksi", back_populates="detail_approval")

    def __repr__(self):
        return (
            f"<DetailApprovalKoreksi(id={self.id}, approval_koreksi_id='{self.approval_koreksi_id}', time='{self.time}', "
            f"type={self.type})>"
        )