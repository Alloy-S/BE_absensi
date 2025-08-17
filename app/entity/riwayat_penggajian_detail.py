from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class RiwayatPenggajianDetail(db.Model):
    __tablename__ = 'riwayat_penggajian_detail'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    total_tunjangan = db.Column(db.Numeric(15,2), nullable=False)
    total_potongan = db.Column(db.Numeric(15,2), nullable=False)
    gaji = db.Column(db.Numeric(15,2), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    riwayat_penggajian_id = db.Column(UUID(as_uuid=True), db.ForeignKey('riwayat_penggajian.id'), nullable=False)

    riwayat_penggajian = db.relationship("RiwayatPenggajian", back_populates="riwayat_penggajian_detail")
    user = db.relationship("Users", back_populates="riwayat_penggajian_detail", lazy="select")
    riwayat_penggajian_rincian = db.relationship("RiwayatPenggajianRincian", back_populates="riwayat_penggajian_detail")