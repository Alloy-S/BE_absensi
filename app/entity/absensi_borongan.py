from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class AbsensiBorongan(db.Model):
    __tablename__ = 'absensi_borongan'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    total = db.Column(db.Numeric(9,2), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    date = db.Column(db.Date, nullable=False, default=db.func.current_timestamp())

    approval_absensi_borongan = db.relationship("ApprovalAbsensiBorongan", back_populates="absensi_borongan", lazy="joined")
    detail_absensi_borongan = db.relationship("DetailAbsensiBorongan", back_populates="absensi_borongan", lazy="joined")
    
    def __repr__(self):
        return (f"<AbsensiBorongan(id={self.id}, total={self.total}, created_date={self.created_date})>, "
                f"date='{self.date}')>")