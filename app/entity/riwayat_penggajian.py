from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class RiwayatPenggajian(db.Model):
    __tablename__ = 'riwayat_penggajian'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    periode_start = db.Column(db.Date, nullable=False)
    periode_end = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(15), nullable=False)
    total_karyawan = db.Column(db.Integer, nullable=False)
    total_gaji_keseluruhan = db.Column(db.Numeric(15,2), nullable=False)
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    date_created =  db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    date_updated = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    grup_gaji_id = db.Column(UUID(as_uuid=True), db.ForeignKey('grup_gaji.id'), nullable=False)

    grup_gaji = db.relationship("GrupGaji", back_populates="riwayat_penggajian", lazy="select")
    riwayat_penggajian_detail = db.relationship("RiwayatPenggajianDetail", back_populates="riwayat_penggajian")
    user = db.relationship("Users", back_populates="riwayat_penggajian", lazy="select")
